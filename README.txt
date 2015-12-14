use Python 3.4

Start django project with any name
cd to project folder
git clone this repo
change setting.py
            
            INSTALLED_APPS = (
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'ceasar'
            )
            
            
            TEMPLATES = [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'DIRS': [os.path.join(BASE_DIR,'templates')],  # IMPORTANT
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            'django.template.context_processors.debug',
                            'django.template.context_processors.request',
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',
                        ],
                    },
                },
            ]
            
            
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                }
            }
            
            STATIC_URL = '/static/'
Change urls.py 

            from ceasar import urls as ceasar_urls

            urlpatterns = [
            
                url(r'^light_it/', include(ceasar_urls)),
            ]
            
copy db.sqlite3 from repo to root of project folder
run server
visit server adress/light_it/
