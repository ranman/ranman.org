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
            listItem.innerHTML = [
                '<a href="',
                proj.html_url,
                '" title="',
                proj.description,
                '">',
                proj.name,
                '</a> - ',
                (proj.description || '')
            ].join('')
            container.appendChild(listItem);
        }
        projects.appendChild(container);
    }, false);
    xhr.send();
}