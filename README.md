Py2captcha
==========

Client library for solve captchas with 2captcha.com support. 
Only support Google Recaptcha new method.

Getting Started
---------------

Install as standard Python package using:

    python setup.py install

Usage
-----

        key = "Your key goes here"
        google_key = "Google recaptcha key"
        url = "http://site.com/captchaurl"
        
        # Create client
        client = TwoCaptchaClient(client_key=key)
        
        # Create Recaptcha Task
        task = ReCaptchav2NewMethod(googlekey=google_key, pageurl=url)
        job = client.createTask(task)
        
        # Wait until captcha is solved
        job.join()
        
        # Result
        value = job.get_solution_response()
        
        # Cost (Always 2.9/1000)
        cost = job.get_solution_cost()
        
        # Base 5 solution time
        time = job.get_solution_time()
