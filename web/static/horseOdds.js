const socket = io();
// const socket = io.connect("http://127.0.0.1:5000", {
// 	transport: ["websocket"],
// });

socket.on("connect", () => {
	console.log("[INFO]: Client connected to Server. Client ID = " + socket.id);
});
