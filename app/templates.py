# Contains all your HTML templates (BASE_TEMPLATE, INDEX_TEMPLATE, FILE_EXPLORER_TEMPLATE, BEHAVIORS_TEMPLATE)
# HTML Templates
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }} - {{ username }}'s Atom Instance</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <style>
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .card-hover {
            transition: all 0.3s ease;
        }
        .card-hover:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body class="bg-gray-50">
    <nav class="bg-black shadow-lg border-b border-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
            <div class="flex items-center space-x-8">
                <div class="flex items-center">
                    <a href="/{{ username }}/home" class="flex items-center space-x-3">
                        <img src="{{ url_for('static', filename='images/atom2.gif') }}" 
                             alt="Atom Logo" 
                             class="h-10 w-10">
                        <span class="text-white text-xl">{{ username }}'s Atom</span>
                    </a>
                </div>
                <!-- Desktop Navigation -->
                <div class="hidden md:flex items-center space-x-6">
                    <a href="/{{ username }}/home" 
                       class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-800 transition-colors">
                        <i class="fas fa-home mr-2"></i>Home
                    </a>
                    <a href="/{{ username }}/files" 
                       class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-800 transition-colors">
                        <i class="fas fa-folder mr-2"></i>Files
                    </a>
                    <a href="/{{ username }}/behaviors" 
                       class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-800 transition-colors">
                        <i class="fas fa-cogs mr-2"></i>Behaviors
                    </a>
                </div>
            </div>
            
            <div class="flex items-center space-x-4">
                <!-- Mobile menu button -->
                <div class="md:hidden">
                    <button id="mobile-menu-button" class="text-gray-300 hover:text-white focus:outline-none focus:text-white">
                        <i class="fas fa-bars text-xl"></i>
                    </button>
                </div>
                
                {% if current_user_email %}
                <div class="hidden sm:block text-sm text-gray-300">
                    <i class="fas fa-user-circle mr-1"></i>
                    {{ current_user_email }}
                </div>
                <a href="/{{ username }}/logout" 
                   class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors">
                    <i class="fas fa-sign-out-alt mr-1"></i>
                    <span class="hidden sm:inline">Logout</span>
                    <span class="sm:hidden">
                        <i class="fas fa-sign-out-alt"></i>
                    </span>
                </a>
                {% endif %}
            </div>
        </div>
        
        <!-- Mobile Navigation Menu -->
        <div id="mobile-menu" class="md:hidden hidden">
            <div class="px-2 pt-2 pb-3 space-y-1 border-t border-gray-800">
                <a href="/{{ username }}/home" 
                   class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-800 transition-colors">
                    <i class="fas fa-home mr-2"></i>Home
                </a>
                <a href="/{{ username }}/files" 
                   class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-800 transition-colors">
                    <i class="fas fa-folder mr-2"></i>Files
                </a>
                <a href="/{{ username }}/behaviors" 
                   class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-800 transition-colors">
                    <i class="fas fa-cogs mr-2"></i>Behaviors
                </a>
                {% if current_user_email %}
                <div class="px-3 py-2 text-sm text-gray-300 border-t border-gray-800 mt-2 pt-2">
                    <i class="fas fa-user-circle mr-1"></i>
                    {{ current_user_email }}
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</nav>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900">{{ title }}</h1>
            {% if subtitle %}
            <p class="mt-2 text-lg text-gray-600">{{ subtitle }}</p>
            {% endif %}
        </div>
        
        <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
            <div class="px-6 py-6">
                {{ content | safe }}
            </div>
        </div>
        
        {% if instance_status %}
        <div class="mt-6 p-4 rounded-lg {% if instance_status == 'online' %}bg-green-50 border border-green-200{% else %}bg-yellow-50 border border-yellow-200{% endif %}">
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    {% if instance_status == 'online' %}
                        <i class="fas fa-circle text-green-400"></i>
                    {% else %}
                        <i class="fas fa-circle text-yellow-400"></i>
                    {% endif %}
                </div>
                <div class="ml-3">
                    <p class="text-sm font-medium {% if instance_status == 'online' %}text-green-800{% else %}text-yellow-800{% endif %}">
                        Instance Status: 
                        {% if instance_status == 'online' %}
                            Online
                        {% else %}
                            Offline (showing cached data)
                        {% endif %}
                    </p>
                </div>
            </div>
        </div>
        {% endif %}
    </div>

    <script>
// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            
            // Toggle icon between hamburger and X
            const icon = mobileMenuButton.querySelector('i');
            if (mobileMenu.classList.contains('hidden')) {
                icon.className = 'fas fa-bars text-xl';
            } else {
                icon.className = 'fas fa-times text-xl';
            }
        });
    }
});
</script>
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
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <style>
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .card-hover {
            transition: all 0.3s ease;
        }
        .card-hover:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Add the navbar here -->
    <nav class="bg-black shadow-lg border-b border-gray-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center space-x-8">
                    <div class="flex items-center">
                        <a href="/" class="flex items-center space-x-3">
                            <img src="{{ url_for('static', filename='images/atom2.gif') }}" 
                                 alt="Atom Logo" 
                                 class="h-10 w-10">
                            <span class="font-bold text-white text-xl">Atom Server</span>
                        </a>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <div class="text-sm text-gray-300">
                        <i class="fas fa-server mr-1"></i>
                        Exposure Server
                    </div>
                </div>
            </div>
        </div>
    </nav>
    
    <div class="gradient-bg py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center">
                <h1 class="text-4xl font-bold text-white mb-4">Atom Exposure Server</h1>
                <p class="text-xl text-white opacity-90">Active Atom Instances</p>
            </div>
        </div>
    </div>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {% if instances %}
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {% for instance in instances %}
                    <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200 card-hover">
                        <div class="flex items-center mb-4">
                            <div class="bg-blue-100 rounded-full p-3 mr-4">
                                <i class="fas fa-atom text-blue-600 text-xl"></i>
                            </div>
                            <h2 class="text-xl font-semibold text-gray-900">{{ instance.username }}</h2>
                        </div>
                        <p class="text-gray-600 mb-4">Atom Instance</p>
                        <a href="/{{ instance.username }}/home" 
                           class="inline-flex items-center justify-center w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors">
                            <i class="fas fa-external-link-alt mr-2"></i>
                            View Instance
                        </a>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="text-center py-12">
                <div class="bg-white rounded-xl shadow-md p-8 max-w-md mx-auto">
                    <i class="fas fa-atom text-gray-400 text-6xl mb-4"></i>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">No Active Instances</h3>
                    <p class="text-gray-600">No Atom instances are currently available.</p>
                </div>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

BEHAVIORS_TEMPLATE = """
<div class="space-y-6">
    <!-- Debug Info (remove this once working) -->
    <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
        <h4 class="font-medium text-yellow-800 mb-2">Debug Info:</h4>
        <pre class="text-xs text-yellow-700 overflow-auto">{{ behaviors_data | tojson(indent=2) }}</pre>
    </div>

    {% if behaviors_data %}
        {% if behaviors_data is mapping %}
            <!-- If behaviors_data is a dictionary -->
            {% if behaviors_data.get('behaviors') %}
                <div class="mb-8">
                    <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                        <i class="fas fa-cogs text-blue-600 mr-2"></i>
                        Behaviors ({{ behaviors_data.behaviors | length }})
                    </h2>
                    <div class="grid gap-6">
                        {% for behavior_name, behavior_steps in behaviors_data.behaviors.items() %}
                            <div class="bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
                                <div class="bg-white px-4 py-3 border-b border-gray-200">
                                    <h3 class="text-lg font-medium text-gray-900 flex items-center">
                                        <i class="fas fa-play-circle text-green-600 mr-2"></i>
                                        {{ behavior_name }}
                                        <span class="ml-2 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                                            {{ behavior_steps | length }} steps
                                        </span>
                                    </h3>
                                </div>
                                <div class="p-4">
                                    <div class="space-y-3">
                                        {% for step in behavior_steps %}
                                            <div class="bg-white rounded-md border border-gray-200 p-3">
                                                <div class="flex items-start space-x-3">
                                                    <div class="flex-shrink-0">
                                                        {% if step.get('type') == 'triggers' %}
                                                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                                <i class="fas fa-bolt mr-1"></i>Trigger
                                                            </span>
                                                        {% else %}
                                                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                                <i class="fas fa-play mr-1"></i>Action
                                                            </span>
                                                        {% endif %}
                                                    </div>
                                                    <div class="flex-1 min-w-0">
                                                        <p class="text-sm font-medium text-gray-900">{{ step.get('name', 'Unknown') }}</p>
                                                        
                                                        {% if step.get('params') %}
                                                            <div class="mt-2">
                                                                <div class="bg-gray-50 rounded p-2">
                                                                    <h5 class="text-xs font-medium text-gray-700 mb-1">Parameters:</h5>
                                                                    <div class="space-y-1">
                                                                        {% for param_key, param_value in step.params.items() %}
                                                                            <div class="text-xs">
                                                                                <span class="font-medium text-gray-600">{{ param_key }}:</span>
                                                                                <span class="text-gray-800 ml-1">
                                                                                    {% if param_value | length > 100 %}
                                                                                        {{ param_value[:100] }}...
                                                                                    {% else %}
                                                                                        {{ param_value }}
                                                                                    {% endif %}
                                                                                </span>
                                                                            </div>
                                                                        {% endfor %}
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        {% endif %}

                                                        {% if step.get('details') %}
                                                            <div class="mt-2">
                                                                <div class="bg-gray-50 rounded p-2">
                                                                    <h5 class="text-xs font-medium text-gray-700 mb-1">Details:</h5>
                                                                    <div class="space-y-1">
                                                                        {% for detail_key, detail_value in step.details.items() %}
                                                                            <div class="text-xs">
                                                                                <span class="font-medium text-gray-600">{{ detail_key }}:</span>
                                                                                <span class="text-gray-800 ml-1">{{ detail_value }}</span>
                                                                            </div>
                                                                        {% endfor %}
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        {% endif %}
                                                        
                                                        {% if step.get('output') %}
                                                            <div class="mt-2">
                                                                <span class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-yellow-100 text-yellow-800">
                                                                    Output: {{ step.output }}
                                                                </span>
                                                            </div>
                                                        {% endif %}
                                                    </div>
                                                </div>
                                            </div>
                                        {% endfor %}
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            {% endif %}

            {% if behaviors_data.get('sequences') %}
                <div class="mb-8">
                    <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                        <i class="fas fa-list-ol text-purple-600 mr-2"></i>
                        Sequences ({{ behaviors_data.sequences | length }})
                    </h2>
                    <div class="grid gap-6">
                        {% for sequence_name, sequence_steps in behaviors_data.sequences.items() %}
                            <div class="bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
                                <div class="bg-white px-4 py-3 border-b border-gray-200">
                                    <h3 class="text-lg font-medium text-gray-900 flex items-center">
                                        <i class="fas fa-tasks text-purple-600 mr-2"></i>
                                        {{ sequence_name }}
                                        <span class="ml-2 px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded-full">
                                            {{ sequence_steps | length }} steps
                                        </span>
                                    </h3>
                                </div>
                                <div class="p-4">
                                    <div class="space-y-3">
                                        {% for step in sequence_steps %}
                                            <div class="bg-white rounded-md border border-gray-200 p-3">
                                                <div class="flex items-start space-x-3">
                                                    <div class="flex-shrink-0">
                                                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                                                            <i class="fas fa-play mr-1"></i>Action
                                                        </span>
                                                    </div>
                                                    <div class="flex-1 min-w-0">
                                                        <p class="text-sm font-medium text-gray-900">{{ step.get('name', 'Unknown') }}</p>
                                                        
                                                        {% if step.get('details') %}
                                                            <div class="mt-2">
                                                                <div class="bg-gray-50 rounded p-2">
                                                                    <h5 class="text-xs font-medium text-gray-700 mb-1">Details:</h5>
                                                                    <div class="space-y-1">
                                                                        {% for detail_key, detail_value in step.details.items() %}
                                                                            <div class="text-xs">
                                                                                <span class="font-medium text-gray-600">{{ detail_key }}:</span>
                                                                                <span class="text-gray-800 ml-1">{{ detail_value }}</span>
                                                                            </div>
                                                                        {% endfor %}
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        {% endif %}

                                                        {% if step.get('params') %}
                                                            <div class="mt-2">
                                                                <div class="bg-gray-50 rounded p-2">
                                                                    <h5 class="text-xs font-medium text-gray-700 mb-1">Parameters:</h5>
                                                                    <div class="space-y-1">
                                                                        {% for param_key, param_value in step.params.items() %}
                                                                            <div class="text-xs">
                                                                                <span class="font-medium text-gray-600">{{ param_key }}:</span>
                                                                                <span class="text-gray-800 ml-1">
                                                                                    {% if param_value | string | length > 100 %}
                                                                                        {{ param_value | string | truncate(100) }}
                                                                                    {% else %}
                                                                                        {{ param_value }}
                                                                                    {% endif %}
                                                                                </span>
                                                                            </div>
                                                                        {% endfor %}
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        {% endif %}
                                                        
                                                        {% if step.get('output') %}
                                                            <div class="mt-2">
                                                                <span class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-yellow-100 text-yellow-800">
                                                                    Output: {{ step.output }}
                                                                </span>
                                                            </div>
                                                        {% endif %}
                                                    </div>
                                                </div>
                                            </div>
                                        {% endfor %}
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            {% endif %}

        {% else %}
            <!-- If behaviors_data is not a dictionary, show it as JSON -->
            <div class="bg-white rounded-lg border border-gray-200 p-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Raw Behaviors Data</h3>
                <pre class="bg-gray-50 rounded p-4 text-sm overflow-auto">{{ behaviors_data | tojson(indent=2) }}</pre>
            </div>
        {% endif %}

    {% else %}
        <div class="text-center py-12">
            <div class="bg-gray-50 rounded-lg p-8">
                <i class="fas fa-cogs text-gray-400 text-6xl mb-4"></i>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">No Behaviors Found</h3>
                <p class="text-gray-600">No behaviors or sequences are currently configured for this instance.</p>
                <p class="text-sm text-gray-500 mt-2">Data received: {{ behaviors_data | string }}</p>
            </div>
        </div>
    {% endif %}
</div>

<style>
/* Custom styles for long content */
.truncate-text {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.expandable {
    cursor: pointer;
}

.expandable:hover {
    background-color: #f9fafb;
}
</style>

<script>
// Add click handlers to expand/collapse long content
document.addEventListener('DOMContentLoaded', function() {
    // Add expand/collapse functionality for long parameter values
    const paramValues = document.querySelectorAll('.param-value');
    paramValues.forEach(function(element) {
        if (element.textContent.length > 100) {
            element.classList.add('expandable');
            element.addEventListener('click', function() {
                this.classList.toggle('truncate-text');
            });
        }
    });
});
</script>
"""

FILE_EXPLORER_TEMPLATE = """
<!-- File Explorer Template with Fixed Path Navigation -->
<div class="flex flex-col h-full">
    <!-- Repository Header -->
    <div class="border-b pb-4 mb-6">
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <h1 class="text-2xl font-semibold text-gray-900 flex items-center">
                    <i class="fas fa-folder-open text-blue-600 mr-3"></i>
                    File Explorer
                </h1>
                <span class="px-3 py-1 text-xs font-medium border border-green-200 bg-green-50 text-green-800 rounded-full">Public</span>
            </div>
        </div>

        <!-- Path Navigation -->
        <div class="flex items-center space-x-4 mt-4">
            <div class="flex-grow">
                <div class="bg-gray-100 rounded-lg px-4 py-2 text-sm breadcrumbs border">
                    <i class="fas fa-home text-gray-500 mr-2"></i>
                    <a href="/{{ username }}/files" class="text-blue-600 hover:text-blue-800 font-medium">root</a>
                    {% if current_path %}
                        {% set path_parts = current_path.split('/') %}
                        {% set accumulated_path = '' %}
                        {% for part in path_parts %}
                            {% if part %}
                                {% if accumulated_path %}
                                    {% set accumulated_path = accumulated_path + '/' + part %}
                                {% else %}
                                    {% set accumulated_path = part %}
                                {% endif %}
                                <span class="text-gray-400 mx-1">/</span>
                                <a href="/{{ username }}/files?path={{ accumulated_path|urlencode }}" class="text-blue-600 hover:text-blue-800 font-medium">{{ part }}</a>
                            {% endif %}
                        {% endfor %}
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <!-- File Explorer -->
    <div class="flex-grow">
        <div class="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <div class="flex items-center justify-between px-6 py-3 bg-gray-50 border-b border-gray-200">
                <div class="flex items-center space-x-4">
                    <button id="uploadBtn" onclick="showUploadModal()" class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">
                        <i class="fas fa-upload mr-2"></i>Upload
                    </button>
                    <button id="newFolderBtn" onclick="showNewFolderModal()" class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">
                        <i class="fas fa-folder-plus mr-2"></i>New Folder
                    </button>
                </div>
            </div>

            <!-- File List -->
            <div class="divide-y divide-gray-200">
                {% if current_path %}
                <div class="flex items-center px-6 py-3 hover:bg-gray-50 transition-colors">
                    <div class="w-1/2 flex items-center">
                        <i class="fas fa-arrow-up text-gray-400 mr-3"></i>
                        <a href="/{{ username }}/files{% if parent_path %}?path={{ parent_path|urlencode }}{% endif %}" class="text-blue-600 hover:text-blue-800 font-medium">Parent Directory</a>
                    </div>
                    <div class="w-1/4 text-center text-gray-500">-</div>
                    <div class="w-1/4 text-center text-gray-500">-</div>
                </div>
                {% endif %}

                {% for item in file_data.folders %}
                <div class="flex items-center px-6 py-3 hover:bg-gray-50 transition-colors">
                    <div class="w-1/2 flex items-center">
                        <i class="fas fa-folder text-yellow-500 mr-3 text-lg"></i>
                        {% if current_path %}
                            {% set folder_path = current_path + '/' + item.name %}
                        {% else %}
                            {% set folder_path = item.name %}
                        {% endif %}
                        <a href="/{{ username }}/files?path={{ folder_path|urlencode }}" class="text-gray-900 hover:text-blue-600 font-medium transition-colors">
                            {{ item.name }}
                        </a>
                    </div>
                    <div class="w-1/4 text-center text-gray-500">-</div>
                    <div class="w-1/4 text-right text-gray-500 pr-4">
                        <span class="text-sm">{{ item.modified }}</span>
                    </div>
                </div>
                {% endfor %}

                {% for item in file_data.files %}
                <div class="flex items-center px-6 py-3 hover:bg-gray-50 transition-colors">
                    <div class="w-1/2 flex items-center">
                        <i class="{{ item.icon }} text-gray-500 mr-3"></i>
                        {% if current_path %}
                            {% set file_path = current_path + '/' + item.name %}
                        {% else %}
                            {% set file_path = item.name %}
                        {% endif %}
                        <a href="#" onclick="viewFile('{{ file_path|e }}')" class="text-gray-900 hover:text-blue-600 font-medium transition-colors">
                            {{ item.name }}
                        </a>
                    </div>
                    <div class="w-1/4 text-center text-gray-500">{{ item.size }}</div>
                    <div class="w-1/4 text-right text-gray-500 pr-4">
                        <span class="text-sm">{{ item.modified }}</span>
                    </div>
                </div>
                {% endfor %}

                {% if not file_data.folders and not file_data.files %}
                <div class="flex items-center justify-center px-6 py-12">
                    <div class="text-gray-500 text-center">
                        <i class="fas fa-folder-open text-6xl mb-4 text-gray-300"></i>
                        <h3 class="text-lg font-medium text-gray-900 mb-1">This directory is empty</h3>
                        <p class="text-gray-600">Upload files or create folders to get started.</p>
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>

<!-- File Viewer Modal with HTML View Options -->
<div id="fileViewerModal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50">
    <div class="relative w-full max-w-4xl mx-auto mt-10 bg-white rounded-lg shadow-xl">
        <div class="p-4 border-b flex items-center justify-between bg-gray-50 rounded-t-lg">
            <div>
                <h3 id="viewerFileName" class="text-lg font-medium text-gray-900"></h3>
                <div class="text-sm text-gray-500">
                    <span id="fileCommitInfo">Last accessed {{ datetime.now().strftime('%Y-%m-%d') }}</span>
                </div>
            </div>
            <div class="flex items-center space-x-2">
                <a id="fileDownloadBtn" href="#" class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors">
                    <i class="fas fa-download mr-1"></i>Download
                </a>
                <button onclick="closeFileViewer()" class="text-gray-400 hover:text-gray-600 transition-colors">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
        </div>
        <div class="p-6 max-h-[70vh] overflow-auto">
            <div id="fileContent"></div>
        </div>
    </div>
</div>

<!-- Upload Modal -->
<div id="uploadModal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50">
    <div class="relative w-full max-w-lg mx-auto mt-20 bg-white rounded-lg shadow-xl">
        <div class="p-4 border-b flex items-center justify-between bg-gray-50 rounded-t-lg">
            <h3 class="text-lg font-medium text-gray-900">Upload Files</h3>
            <button onclick="closeUploadModal()" class="text-gray-400 hover:text-gray-600 transition-colors">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="p-6">
            <form id="uploadForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Select Files</label>
                    <input type="file" id="fileInput" multiple 
                           class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Current Directory</label>
                    <div class="text-sm text-gray-600 bg-gray-50 px-3 py-2 rounded-md border">
                        /{{ current_path if current_path else 'root' }}
                    </div>
                </div>
                <div id="uploadStatus" class="text-sm"></div>
                <div class="flex justify-end space-x-3 pt-4">
                    <button type="button" onclick="closeUploadModal()" 
                            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors">
                        Cancel
                    </button>
                    <button type="button" onclick="uploadFiles()" 
                            class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
                        Upload
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- New Folder Modal -->
<div id="newFolderModal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50">
    <div class="relative w-full max-w-md mx-auto mt-20 bg-white rounded-lg shadow-xl">
        <div class="p-4 border-b flex items-center justify-between bg-gray-50 rounded-t-lg">
            <h3 class="text-lg font-medium text-gray-900">Create New Folder</h3>
            <button onclick="closeNewFolderModal()" class="text-gray-400 hover:text-gray-600 transition-colors">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="p-6">
            <form id="newFolderForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Folder Name</label>
                    <input type="text" id="folderNameInput" 
                           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500" required>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Current Directory</label>
                    <div class="text-sm text-gray-600 bg-gray-50 px-3 py-2 rounded-md border">
                        /{{ current_path if current_path else 'root' }}
                    </div>
                </div>
                <div class="flex justify-end space-x-3 pt-4">
                    <button type="button" onclick="closeNewFolderModal()" 
                            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors">
                        Cancel
                    </button>
                    <button type="button" onclick="createFolder()" 
                            class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
                        Create
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
// Global variable to store current path for use in JavaScript functions
const currentPath = '{{ current_path|e }}';
const username = '{{ username|e }}';

function viewFile(filePath) {
    console.log('Viewing file:', filePath);
    
    // Try to fetch from our server-side cache first
    fetch(`/${username}/file-content/${encodeURIComponent(filePath)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('File content not available');
            }
            return response.json();
        })
        .then(data => {
            displayFileContent(data, filePath);
        })
        .catch(error => {
            console.error('Error:', error);
            // Show a user-friendly error message
            document.getElementById('fileContent').innerHTML = `
                <div class="text-center text-red-500">
                    <i class="fas fa-exclamation-triangle text-4xl mb-2"></i>
                    <p>Failed to load file content</p>
                    <p class="text-sm">${error.message}</p>
                </div>
            `;
            document.getElementById('viewerFileName').textContent = filePath.split('/').pop();
            document.getElementById('fileViewerModal').classList.remove('hidden');
        });
}

function displayFileContent(data, filePath) {
    document.getElementById('viewerFileName').textContent = data.filename;
    const contentDiv = document.getElementById('fileContent');
    
    // Set up download button with improved handling for all file types
    const downloadBtn = document.getElementById('fileDownloadBtn');
    
    // Remove any existing event listeners
    downloadBtn.replaceWith(downloadBtn.cloneNode(true));
    const newDownloadBtn = document.getElementById('fileDownloadBtn');
    
    newDownloadBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        try {
            // Handle different content formats based on file type
            let binaryContent;
            
            // For text files, we might need special handling
            if (data.mime_type.startsWith('text/') || 
                data.mime_type === 'application/json' || 
                data.mime_type === 'application/javascript') {
                
                try {
                    // First try to decode as base64
                    binaryContent = atob(data.content);
                } catch (decodeError) {
                    // If not valid base64, use the content directly
                    // Convert string content to binary
                    const encoder = new TextEncoder();
                    binaryContent = String.fromCharCode(...encoder.encode(data.content));
                }
            } else {
                // For binary files, decode from base64
                binaryContent = atob(data.content);
            }
            
            // Convert to array buffer
            const bytes = new Uint8Array(binaryContent.length);
            for (let i = 0; i < binaryContent.length; i++) {
                bytes[i] = binaryContent.charCodeAt(i);
            }
            
            // Create blob and download
            const blob = new Blob([bytes], {type: data.mime_type || 'application/octet-stream'});
            const url = window.URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            
            // Clean up
            setTimeout(() => {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }, 100);
        } catch (err) {
            console.error("Download error:", err);
            alert("There was a problem downloading the file. Please try again.");
        }
    });
    
    // Check if it's an HTML file and provide view options
    if (data.filename.endsWith('.html') || data.mime_type === 'text/html') {
        // Create toggle buttons for raw/rendered view
        const viewOptionsHtml = `
            <div class="mb-4 flex space-x-2">
                <button id="viewRawBtn" class="px-3 py-1 border rounded bg-gray-100 hover:bg-gray-200 transition-colors">View Raw</button>
                <button id="viewRenderedBtn" class="px-3 py-1 border rounded hover:bg-gray-100 transition-colors">View Rendered</button>
            </div>
            <div id="rawContentView" class="block">
                <pre class="whitespace-pre-wrap p-4 bg-gray-50 rounded border overflow-auto">${escapeHtml(data.content)}</pre>
            </div>
        `;
        
        contentDiv.innerHTML = viewOptionsHtml;
        
        // Add event listeners to toggle buttons
        setTimeout(() => {
            document.getElementById('viewRawBtn').addEventListener('click', function() {
                document.getElementById('rawContentView').classList.remove('hidden');
                document.getElementById('viewRawBtn').classList.add('bg-gray-100');
                document.getElementById('viewRenderedBtn').classList.remove('bg-gray-100');
            });
            
            document.getElementById('viewRenderedBtn').addEventListener('click', function() {
                // Open in new window
                const newWindow = window.open('', '_blank');
                newWindow.document.write(data.content);
                newWindow.document.close();
            });
        }, 0);
    } else if (data.mime_type.startsWith('image/')) {
        contentDiv.innerHTML = `<div class="text-center"><img src="data:${data.mime_type};base64,${data.content}" class="max-w-full max-h-96 mx-auto rounded-lg shadow-md"></div>`;
    } else if (data.mime_type.startsWith('text/') || data.mime_type === 'application/json' || 
               data.mime_type === 'application/javascript') {
        contentDiv.innerHTML = `<pre class="whitespace-pre-wrap p-4 bg-gray-50 rounded border overflow-auto" style="max-height: 500px;">${escapeHtml(data.content)}</pre>`;
    } else {
        contentDiv.innerHTML = `<div class="text-center">
            <i class="fas fa-file text-6xl text-gray-400 mb-4"></i>
            <p class="text-lg">File type: ${data.mime_type}</p>
            <p class="mt-2 text-gray-600">Click the download button above to download this file.</p>
        </div>`;
    }
    
    document.getElementById('fileViewerModal').classList.remove('hidden');
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function closeFileViewer() {
    document.getElementById('fileViewerModal').classList.add('hidden');
    document.getElementById('fileContent').innerHTML = '';
}

// Upload functionality
function showUploadModal() {
    console.log('showUploadModal called');
    document.getElementById('uploadModal').classList.remove('hidden');
    document.getElementById('uploadStatus').innerHTML = '';
}

function closeUploadModal() {
    document.getElementById('uploadModal').classList.add('hidden');
    document.getElementById('fileInput').value = '';
    document.getElementById('uploadStatus').innerHTML = '';
}

function uploadFiles() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;
    
    if (files.length === 0) {
        document.getElementById('uploadStatus').innerHTML = 
            '<p class="text-red-500">Please select at least one file to upload</p>';
        return;
    }
    
    console.log(`Uploading ${files.length} files to path: ${currentPath}`);
    
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        console.log(`Adding file: ${files[i].name}`);
        formData.append('file', files[i]);
    }
    
    // Add current path
    formData.append('path', currentPath);
    
    document.getElementById('uploadStatus').innerHTML = 
        '<p class="text-blue-500">Uploading files...</p>';
    
    fetch(`/${username}/api/upload`, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log(`Response status: ${response.status}`);
        return response.text().then(text => {
            try {
                return JSON.parse(text);
            } catch (e) {
                console.error('Failed to parse JSON response:', text);
                throw new Error(`Server returned non-JSON response: ${text.substring(0, 100)}`);
            }
        });
    })
    .then(data => {
        console.log('Upload response:', data);
        if (data.status === 'success') {
            document.getElementById('uploadStatus').innerHTML = 
                '<p class="text-green-500">Files uploaded successfully!</p>';
            
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            document.getElementById('uploadStatus').innerHTML = 
                `<p class="text-red-500">Upload failed: ${data.error || 'Unknown error'}</p>`;
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        document.getElementById('uploadStatus').innerHTML = 
            `<p class="text-red-500">Upload failed: ${error.message}</p>`;
    });
}

// New folder functionality
function showNewFolderModal() {
    console.log('showNewFolderModal called');
    document.getElementById('newFolderModal').classList.remove('hidden');
    document.getElementById('folderNameInput').value = '';
}

function closeNewFolderModal() {
    document.getElementById('newFolderModal').classList.add('hidden');
}

function createFolder() {
    const folderName = document.getElementById('folderNameInput').value.trim();
    
    if (!folderName) {
        alert('Please enter a folder name');
        return;
    }
    
    console.log(`Creating folder: ${folderName} in path: ${currentPath}`);
    
    const formData = new FormData();
    formData.append('path', currentPath);
    formData.append('folder', JSON.stringify({ name: folderName }));
    
    fetch(`/${username}/api/upload`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            closeNewFolderModal();
            // Reload the page to show the new folder
            window.location.reload();
        } else {
            alert(`Failed to create folder: ${data.error || 'Unknown error'}`);
        }
    })
    .catch(error => {
        console.error('Error creating folder:', error);
        alert('Failed to create folder. Please try again.');
    });
}

// Debug function to check if elements exist
function debugElements() {
    console.log('Upload button:', document.getElementById('uploadBtn'));
    console.log('New folder button:', document.getElementById('newFolderBtn'));
    console.log('Upload modal:', document.getElementById('uploadModal'));
    console.log('New folder modal:', document.getElementById('newFolderModal'));
}

// Call debug function when page loads
console.log('Script loaded, checking elements...');
debugElements();
</script>
"""
