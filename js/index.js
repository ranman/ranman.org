window.onload = function() {
    var projects = document.getElementById('projects-list');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://api.github.com/users/ranman/repos?type=sources&sort=update', true);
    xhr.setRequestHeader('Accept', 'application/vnd.github.v3+json');
    xhr.responseType = 'json';
    xhr.addEventListener('load', function(e) {
        var data = xhr.response;
        var container = document.createDocumentFragment();
        var listItem;
        var proj;
        for(var i=0; i<data.length; i++) {
            proj = data[i];
            listItem = document.createElement('li');
            listItem.innerHTML = '<a href="'+proj.html_url+'" title="'+proj.description+'">'+proj.name+'</a>'
            container.appendChild(listItem);
        }
        projects.appendChild(container);
    }, false);
    xhr.send();
}