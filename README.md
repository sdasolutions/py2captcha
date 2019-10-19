Py2captcha
==========

Client library to solve captchas with 2captcha.com support.

Getting Started
---------------

Install as a standard Python package using:

    pip install py2captcha

Usage
-----
        
        from py2captcha import TwoCaptchaClient, GoogleReCaptchaV2Task
        
        # 2captcha.com authentication key
        key = "Your key goes here"

        # Website data
        google_key = "Google recaptcha key"  # sitekey
        url = "http://site.com/captchaurl"
        
        # Create client
        client = TwoCaptchaClient(client_key=key)
        
        # Create Recaptcha Task
        task = GoogleReCaptchaV2Task(googlekey=google_key, pageurl=url)
        job = client.create_task(task)
        
        # Wait until captcha is solved
        job.join()
        
        # Result
        value = job.get_solution_response()
        
        # Cost (Always 2.9/1000)
        cost = job.get_solution_cost()
        
        # Base 5 solution time
        time = job.get_solution_time()

Supported CAPTCHA types
-----------------------

**reCAPTCHA V2**