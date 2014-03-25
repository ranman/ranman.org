window.onload = function() {
	var projects = document.getElementById('projects-list');
	var xhr = new XMLHttpRequest();
	xhr.open('GET', 'https://api.github.com/search/repositories?q=user:ranman&sort=updated&per_page=100', true);
	xhr.setRequestHeader('Accept', 'application/vnd.github.v3+json');
	xhr.responseType = 'json';
	xhr.addEventListener('load', function(e) {
		var data = xhr.response.items;
		var container = document.createDocumentFragment();
		var listItem;
		var proj;
		for(var i=0; i<data.length; i++) {
			proj = data[i];
			listItem = document.createElement('li');
			listItem.className = "project";
			listItem.innerHTML = [
				'<a href="',
				proj.html_url,
				'" title="',
				proj.description,
				'">',
				proj.name,
				'</a> - ',
				(proj.description || '')
			].join('');
			listItem.dataset.index = proj.name.toLowerCase().replace(' ', '').replace('-', '').replace(',', '').replace('!', '')
			container.appendChild(listItem);
		}
		projects.appendChild(container);
	}, false);
	xhr.send();
	createSearcher(
		document.getElementById('projects-search'),
		document.getElementById('projects-search-style'),
		".project");
	createSearcher(
		document.getElementById('speaking-search'),
		document.getElementById('speaking-search-style'),
		".speaking");
}
function createSearcher(elem, style, selector) {
	elem.addEventListener('input', function() {
		if (!this.value) {
			style.innerHTML = "";
			return;
		}
		style.innerHTML = selector+":not([data-index*=\"" + this.value.toLowerCase() + "\"]) { display: none; }";
	})
}