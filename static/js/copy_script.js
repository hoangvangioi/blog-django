function copyTextToClipboard(text) {
	var textArea = document.createElement('textarea');

	// Place in the top-left corner of screen regardless of scroll position.
	textArea.style.position = 'fixed';
	textArea.style.top = 0;
	textArea.style.left = 0;

	textArea.style.width = '2em';
	textArea.style.height = '2em';

	textArea.style.padding = 0;

	// Clean up any borders.
	textArea.style.border = 'none';
	textArea.style.outline = 'none';
	textArea.style.boxShadow = 'none';

	// Avoid flash of the white box if rendered for any reason.
	textArea.style.background = 'transparent';

	textArea.value = text;

	document.body.appendChild(textArea);
	textArea.focus();
	textArea.select();

	try {
		document.execCommand('copy');
	} catch (err) {
		console.log('unable to copy');
	}

	document.body.removeChild(textArea);
}

var copyBtn = document.querySelector('[data-copy-btn="buttonCopy"]');

copyBtn.addEventListener('click', function (event) {
	var url = copyBtn.getAttribute('data-copy-url');
	copyTextToClipboard(url);
});
