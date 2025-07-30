use pyo3::prelude::*;
use std::sync::Arc;
use tokio::sync::Mutex;
use tokio_tungstenite::{connect_async, WebSocketStream, MaybeTlsStream};
use tokio_tungstenite::tungstenite::Message;
use futures::{SinkExt, StreamExt};
use url::Url;
use std::collections::HashMap;
use tokio::time::timeout;
use std::time::Duration;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc as StdArc;
use tokio::time::sleep;

type WsStream = WebSocketStream<MaybeTlsStream<tokio::net::TcpStream>>;

#[pyclass]
pub struct WebSocketClient {
    callbacks: Arc<Mutex<Callbacks>>,
    connections: Arc<Mutex<HashMap<String, WebSocketConnection>>>,
    running: StdArc<AtomicBool>,
}

struct WebSocketConnection {
    stream: Arc<Mutex<WsStream>>,
}

#[derive(Default)]
struct Callbacks {
    on_message: Option<PyObject>,
    on_open: Option<PyObject>,
    on_close: Option<PyObject>,
}

impl WebSocketClient {
    async fn handle_messages(connection_id: String, stream: Arc<Mutex<WsStream>>, callbacks: Arc<Mutex<Callbacks>>, running: StdArc<AtomicBool>) {
        let mut ping_interval = tokio::time::interval(Duration::from_secs(30));

        while running.load(Ordering::SeqCst) {
            tokio::select! {
                _ = ping_interval.tick() => {
                    if !running.load(Ordering::SeqCst) {
                        break;
                    }
                    if let Ok(mut stream_lock) = timeout(Duration::from_secs(1), stream.lock()).await {
                        if let Err(_) = stream_lock.send(Message::Ping(vec![])).await {
                            break;
                        }
                    }
                }
                _ = async {
                    while running.load(Ordering::SeqCst) {
                        sleep(Duration::from_millis(100)).await;
                    }
                } => {
                    break;
                }
                msg = async {
                    if let Ok(mut stream_lock) = timeout(Duration::from_secs(1), stream.lock()).await {
                        timeout(Duration::from_secs(1), stream_lock.next()).await.ok().flatten()
                    } else {
                        None
                    }
                } => {
                    match msg {
                        Some(Ok(Message::Text(text))) => {
                            if let Some(on_message) = &callbacks.lock().await.on_message {
                                let connection_id_clone = connection_id.clone();
                                let text_clone = text.clone();

                                // 获取Python的异步上下文
                                if let Ok(locals) = Python::with_gil(|py| {
                                    pyo3_asyncio::tokio::get_current_locals(py)
                                }) {
                                    // 调用回调函数并检查返回值
                                    if let Ok(fut) = Python::with_gil(|py| {
                                        match on_message.call1(py, (connection_id_clone, text_clone)) {
                                            Ok(future) => {
                                                // 尝试将返回值转换为Rust的Future
                                                pyo3_asyncio::tokio::into_future(future.as_ref(py))
                                            }
                                            Err(e) => Err(e)
                                        }
                                    }) {
                                        // 等待Future完成
                                        let _ = pyo3_asyncio::tokio::scope(locals, fut).await;
                                    }
                                }
                            }
                        }
                        Some(Ok(Message::Ping(data))) => {
                            if let Ok(mut stream_lock) = timeout(Duration::from_secs(1), stream.lock()).await {
                                let _ = stream_lock.send(Message::Pong(data)).await;
                            }
                        }
                        Some(Ok(Message::Close(_))) => {
                            break;
                        }
                        Some(Err(_)) => {
                            break;
                        }
                        None => {
                            if !running.load(Ordering::SeqCst) {
                                break;
                            }
                        }
                        _ => {}
                    }
                }
            }
        }

        if let Ok(mut stream_lock) = timeout(Duration::from_secs(1), stream.lock()).await {
            let _ = stream_lock.send(Message::Close(None)).await;
        }
    }
}

#[pymethods]
impl WebSocketClient {
    #[new]
    fn new() -> Self {
        WebSocketClient {
            callbacks: Arc::new(Mutex::new(Callbacks::default())),
            connections: Arc::new(Mutex::new(HashMap::new())),
            running: StdArc::new(AtomicBool::new(true)),
        }
    }

    fn set_on_message(&mut self, callback: PyObject) -> PyResult<()> {
        let mut callbacks = self.callbacks.blocking_lock();
        callbacks.on_message = Some(callback);
        Ok(())
    }

    fn set_on_open(&mut self, callback: PyObject) -> PyResult<()> {
        let mut callbacks = self.callbacks.blocking_lock();
        callbacks.on_open = Some(callback);
        Ok(())
    }

    fn set_on_close(&mut self, callback: PyObject) -> PyResult<()> {
        let mut callbacks = self.callbacks.blocking_lock();
        callbacks.on_close = Some(callback);
        Ok(())
    }

    fn connect<'p>(&mut self, py: Python<'p>, url: String, connection_id: String) -> PyResult<&'p PyAny> {
        let callbacks = self.callbacks.clone();
        let connections = self.connections.clone();
        let running = self.running.clone();

        pyo3_asyncio::tokio::future_into_py(py, async move {
            let url = Url::parse(&url).map_err(|e| {
                PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string())
            })?;

            let (ws_stream, _) = connect_async(url).await.map_err(|e| {
                PyErr::new::<pyo3::exceptions::PyConnectionError, _>(e.to_string())
            })?;

            let stream = Arc::new(Mutex::new(ws_stream));

            let connection_id_clone = connection_id.clone();
            let callbacks_clone = callbacks.clone();
            let stream_clone = stream.clone();

            tokio::spawn(async move {
                Self::handle_messages(connection_id_clone, stream_clone, callbacks_clone, running).await;
            });

            let mut connections = connections.lock().await;
            connections.insert(connection_id.clone(), WebSocketConnection { stream });

            if let Some(on_open) = &callbacks.lock().await.on_open {
                Python::with_gil(|py| {
                    let _ = on_open.call1(py, (connection_id.clone(),));
                });
            }

            Ok(())
        })
    }

    fn send<'p>(&self, py: Python<'p>, message: String, connection_id: String) -> PyResult<&'p PyAny> {
        let connections = self.connections.clone();

        pyo3_asyncio::tokio::future_into_py(py, async move {
            let connections = connections.lock().await;
            if let Some(conn) = connections.get(&connection_id) {
                let stream_lock = timeout(Duration::from_secs(5), conn.stream.lock()).await
                    .map_err(|_| {
                        PyErr::new::<pyo3::exceptions::PyTimeoutError, _>("获取流锁超时")
                    })?;

                let mut stream = stream_lock;
                match timeout(Duration::from_secs(5), stream.send(Message::Text(message))).await {
                    Ok(result) => {
                        result.map_err(|e| {
                            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string())
                        })?;
                    }
                    Err(_) => {
                        return Err(PyErr::new::<pyo3::exceptions::PyTimeoutError, _>("发送消息超时"));
                    }
                }
            } else {
                return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("连接不存在"));
            }
            Ok(())
        })
    }

    fn close<'p>(&self, py: Python<'p>, connection_id: String) -> PyResult<&'p PyAny> {
        let connections = self.connections.clone();
        let callbacks = self.callbacks.clone();

        pyo3_asyncio::tokio::future_into_py(py, async move {
            let connections = connections.lock().await;
            if let Some(conn) = connections.get(&connection_id) {
                if let Ok(mut stream_lock) = timeout(Duration::from_secs(1), conn.stream.lock()).await {
                    let _ = stream_lock.send(Message::Close(None)).await;
                }
            }

            let mut connections = connections;
            if let Some(_) = connections.remove(&connection_id) {
                if let Some(on_close) = &callbacks.lock().await.on_close {
                    Python::with_gil(|py| {
                        let _ = on_close.call1(py, (connection_id,));
                    });
                }
            }
            Ok(())
        })
    }

    fn stop(&self) {
        self.running.store(false, Ordering::SeqCst);
    }

    fn run_forever<'p>(&self, py: Python<'p>, url: String, connection_id: String) -> PyResult<&'p PyAny> {
        let client = self.clone();
        self.running.store(true, Ordering::SeqCst);

        pyo3_asyncio::tokio::future_into_py::<_, ()>(py, async move {
            while client.running.load(Ordering::SeqCst) {
                match WebSocketClient::connect_and_run(&client, &url, &connection_id).await {
                    Ok(_) | Err(_) => {
                        if client.running.load(Ordering::SeqCst) {
                            tokio::time::sleep(Duration::from_secs(5)).await;
                        }
                    }
                }
            }
            Ok(())
        })
    }
}

impl WebSocketClient {
    fn clone(&self) -> Self {
        WebSocketClient {
            callbacks: self.callbacks.clone(),
            connections: self.connections.clone(),
            running: self.running.clone(),
        }
    }

    async fn connect_and_run(client: &WebSocketClient, url: &str, connection_id: &str) -> Result<(), PyErr> {
        let url = Url::parse(url).map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string())
        })?;

        let (ws_stream, _) = connect_async(url).await.map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyConnectionError, _>(e.to_string())
        })?;

        let stream = Arc::new(Mutex::new(ws_stream));

        let connection_id = connection_id.to_string();
        let callbacks = client.callbacks.clone();
        let connections = client.connections.clone();

        let mut conns = connections.lock().await;
        conns.insert(connection_id.clone(), WebSocketConnection { stream: stream.clone() });
        drop(conns);

        if let Some(on_open) = &callbacks.lock().await.on_open {
            let locals = Python::with_gil(|py| {
                pyo3_asyncio::tokio::get_current_locals(py)
            })?;

            let fut = Python::with_gil(|py| {
                match on_open.call1(py, (connection_id.clone(),)) {
                    Ok(future) => {
                        pyo3_asyncio::tokio::into_future(future.as_ref(py))
                    }
                    Err(e) => Err(e)
                }
            })?;

            let _ = pyo3_asyncio::tokio::scope(locals, fut).await;
        }

        Self::handle_messages(
            connection_id.clone(),
            stream.clone(),
            callbacks.clone(),
            client.running.clone()
        ).await;

        let mut conns = connections.lock().await;
        conns.remove(&connection_id);

        Ok(())
    }
}

#[pymodule]
fn _rws(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<WebSocketClient>()?;
    Ok(())
}