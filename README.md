# Py2captcha

Client library to solve captchas with 2captcha.com support.

## Getting Started

Install as a standard Python package using:

    pip install py2captcha

## Usage
        
        from py2captcha import TwoCaptchaClient, GoogleReCaptchaV2Task
        
        # 2captcha.com authentication key
        key = "Your key goes here"

        # Website data
        google_key = "Google recaptcha key"  # sitekey
        url = "http://site.com/captchaurl"
        
        # Create client
        client = TwoCaptchaClient(client_key=key)

        # Requesting 2captcha.com queue status for reCAPTCHA V2
        status = client.get_queue_stats()

        print("reCAPTCHA V2 queue status:")
        print("Total workers: %d" % status.workers_total)
        print("Free workers: %d" % status.free_workers)
        print("Load factor: %d%%" % status.load)
        print("Average solve speed: %d seconds" % status.speed)
        print("Price per 1000 CAPTCHAS: %f USD" % status.bid)

        # Create Recaptcha Task
        task = GoogleReCaptchaV2Task(googlekey=google_key, pageurl=url)
        job = client.create_task(task)

        # Wait until captcha is solved
        # For async runs just call job.check_is_ready() until it returns true
        job.join()

        # Result
        token = job.get_solution_response()

        # Cost (Always 2.9/1000)
        cost = job.get_solution_cost()

        # Base 5 solution time
        time = job.get_solution_time()

        print("Token: %s" % token)
        print("Cost: %f USD" % cost)
        print("Solve time: %d seconds" % time)


## Supported CAPTCHA types

* reCAPTCHA V2