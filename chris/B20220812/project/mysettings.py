DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',    
        'NAME': 'HWMonitoring',                  
        'USER': 'root',                          
        'PASSWORD': 'baro',                  
        'HOST': 'localhost',                     
        'PORT': '3306',  
        'OPTIONS': {
        'init_command' : "SET sql_mode='STRICT_TRANS_TABLES'",
        }                        
    },
}
