import socketio
import threading

class SocketUtility:
    def __init__(self, server_url):
        """Initialize the SocketManager with the server URL."""
        self.server_url = server_url
        self.sio = socketio.Client()
        self._setup_event_handlers()
        self.connect()

    def _setup_event_handlers(self):
        """Register event handlers for the Socket.IO client."""
        @self.sio.event
        def connect():
            print("Connected to the server")

        @self.sio.event
        def disconnect():
            print("Disconnected from the server")

        @self.sio.on('ping')
        def on_welcome(data):
            print("Server ping recieved")

    def connect(self):
        """Connect to the Socket.IO server."""
        threading.Thread(target=self._connect_in_thread, daemon=True).start()

    def _connect_in_thread(self):
        """Handle the connection in a separate thread."""
        self.sio.connect(self.server_url)
        print("Socket.IO client running in background")

    def emit(self, event_name, data):
        """Emit an event to the server."""
        self.sio.emit(event_name, data)
        print(f"Event '{event_name}' emitted with data: {data}")

    def disconnect(self):
        """Disconnect from the Socket.IO server."""
        self.sio.disconnect()

    def register_event_handler(self, event_name, handler):
        """Register a custom event handler."""
        self.sio.on(event_name, handler)

