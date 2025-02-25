# Contains all your HTML templates (BASE_TEMPLATE, INDEX_TEMPLATE, FILE_EXPLORER_TEMPLATE)
# HTML Templates
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }} - {{ username }}'s Atom Instance</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <nav class="bg-white shadow-lg">
        <div class="max-w-6xl mx-auto px-4">
            <div class="flex justify-between">
                <div class="flex space-x-7">
                    <div class="flex items-center py-4">
                        <span class="font-semibold text-gray-500 text-lg">{{ username }}'s Atom</span>
                    </div>
                    <div class="hidden md:flex items-center space-x-1">
                        <a href="/{{ username }}/home" class="py-4 px-2 text-gray-500 hover:text-gray-900">Home</a>
                        <a href="/{{ username }}/files" class="py-4 px-2 text-gray-500 hover:text-gray-900">Files</a>
                        <a href="/{{ username }}/behaviors" class="py-4 px-2 text-gray-500 hover:text-gray-900">Behaviors</a>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-2xl font-bold mb-6">{{ title }}</h1>
        <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
            {{ content | safe }}
        </div>
        
        {% if instance_status %}
        <div class="mt-4 p-4 rounded {% if instance_status == 'online' %}bg-green-100{% else %}bg-yellow-100{% endif %}">
            <p class="text-sm">
                Instance Status: 
                <span class="font-semibold">
                    {% if instance_status == 'online' %}
                        Online
                    {% else %}
                        Offline (showing cached data)
                    {% endif %}
                </span>
            </p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Atom Exposure Server</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-6">Active Atom Instances</h1>
        
        {% if instances %}
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {% for instance in instances %}
                    <div class="bg-white rounded-lg shadow p-6">
                        <h2 class="text-xl font-semibold mb-2">{{ instance.username }}</h2>
                        <div class="space-y-2">
                            <a href="/{{ instance.username }}/home" 
                               class="block w-full text-center bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded">
                                View Instance
                            </a>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="bg-white rounded-lg shadow p-6">
                <p class="text-gray-500">No active instances available.</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""
FILE_EXPLORER_TEMPLATE = """
<div class="mb-4">
    <div class="flex items-center space-x-2 mb-4">
        <div class="bg-gray-200 text-gray-700 px-3 py-1 rounded-md text-sm">
            / {{ current_path }}
        </div>
        <div class="flex-grow"></div>
        <label for="fileUpload" class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm cursor-pointer">
            <i class="fas fa-upload mr-1"></i> Upload
        </label>
        <input type="file" id="fileUpload" class="hidden" multiple>
        <button onclick="createNewFolder()" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm">
            <i class="fas fa-folder-plus mr-1"></i> New Folder
        </button>
    </div>
    
    <div class="bg-white border rounded-md">
        <div class="flex items-center justify-between px-4 py-2 bg-gray-50 border-b font-medium text-sm">
            <div class="w-1/2">Name</div>
            <div class="w-1/4 text-center">Size</div>
            <div class="w-1/4 text-center">Modified</div>
        </div>
        
        {% if current_path != "" %}
        <div class="flex items-center px-4 py-2 border-b hover:bg-gray-50">
            <div class="w-1/2 flex items-center">
                <i class="fas fa-arrow-up text-gray-500 mr-2"></i>
                <a href="/{{ username }}/files?path={{ parent_path }}" class="text-blue-500 hover:underline">...</a>
            </div>
            <div class="w-1/4 text-center text-gray-500">-</div>
            <div class="w-1/4 text-center text-gray-500">-</div>
        </div>
        {% endif %}
        
        {% for item in file_data.folders %}
        <div class="flex items-center px-4 py-2 border-b hover:bg-gray-50">
            <div class="w-1/2 flex items-center">
                <i class="fas fa-folder text-yellow-400 mr-2"></i>
                <a href="/{{ username }}/files?path={{ current_path_prefix }}{{ item.name }}" class="hover:underline">{{ item.name }}</a>
            </div>
            <div class="w-1/4 text-center text-gray-500">-</div>
            <div class="w-1/4 text-center text-gray-500">{{ item.modified }}</div>
        </div>
        {% endfor %}
        
        {% for item in file_data.files %}
        <div class="flex items-center px-4 py-2 border-b hover:bg-gray-50">
            <div class="w-1/2 flex items-center">
                <i class="{{ item.icon }} mr-2 text-gray-500"></i>
                <a href="#" onclick="viewFile('{{ current_path_prefix }}{{ item.name }}')" class="hover:underline">{{ item.name }}</a>
            </div>
            <div class="w-1/4 text-center text-gray-500">{{ item.size }}</div>
            <div class="w-1/4 text-center text-gray-500">{{ item.modified }}</div>
        </div>
        {% endfor %}
    </div>
</div>

<!-- File Viewer Modal -->
<div id="fileViewerModal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50">
    <div class="relative w-full max-w-4xl mx-auto mt-10 bg-white rounded-lg">
        <div class="p-4 border-b">
            <h3 id="viewerFileName" class="text-lg font-medium"></h3>
            <button onclick="closeFileViewer()" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="p-4 max-h-[70vh] overflow-auto">
            <div id="fileContent"></div>
        </div>
    </div>
</div>

<script>
document.getElementById('fileUpload').addEventListener('change', function(e) {
    const files = e.target.files;
    if (files.length > 0) {
        uploadFiles(files);
    }
});

function uploadFiles(files) {
    const formData = new FormData();
    formData.append('path', '{{ current_path }}');
    
    for (let file of files) {
        formData.append('file', file);
    }

    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.reload();
        } else {
            alert('Upload failed: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Upload failed');
    });
}

function createNewFolder() {
    const folderName = prompt('Enter folder name:');
    if (folderName) {
        const formData = new FormData();
        formData.append('path', '{{ current_path }}');
        formData.append('folder', JSON.stringify({ name: folderName }));

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.reload();
            } else {
                alert('Failed to create folder: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to create folder');
        });
    }
}

function viewFile(filePath) {
    fetch(`/api/files/${filePath}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('viewerFileName').textContent = data.filename;
            const contentDiv = document.getElementById('fileContent');
            
            if (data.mime_type.startsWith('image/')) {
                contentDiv.innerHTML = `<img src="data:${data.mime_type};base64,${data.content}" class="max-w-full">`;
            } else if (data.mime_type.startsWith('text/') || data.mime_type === 'application/json') {
                contentDiv.innerHTML = `<pre class="whitespace-pre-wrap">${data.content}</pre>`;
            } else {
                contentDiv.innerHTML = `<div class="text-center">
                    <p>File type: ${data.mime_type}</p>
                    <a href="data:${data.mime_type};base64,${data.content}" 
                       download="${data.filename}" 
                       class="bg-blue-500 text-white px-4 py-2 rounded mt-4 inline-block">
                        Download File
                    </a>
                </div>`;
            }
            
            document.getElementById('fileViewerModal').classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load file');
        });
}

function closeFileViewer() {
    document.getElementById('fileViewerModal').classList.add('hidden');
    document.getElementById('fileContent').innerHTML = '';
}
</script>
"""