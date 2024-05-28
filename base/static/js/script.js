// hiding the message.
function hiding_message() {
	let message = document.getElementById('msg_tag');

	message.style.display = 'none';
}
let interval = setInterval(hiding_message, 3000);