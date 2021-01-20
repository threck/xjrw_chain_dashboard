# API_Automation_Test
>pip3 install virtualenv
>virtualenv venv
>source venv/bin/activate

## need to install some libraries:
>pip3 install pytest pytest-html allure-pytest pymongo requests requests-toolbelt websocket-client base58 pytz

>pip3 install websockets asyncio
## how to run auto api testcase:
>python run.py

## exit python venv
>deactivate

## not needed
>pip3 install PyYaml faker

### how to run pytest cases with marks
>pytest -m http  # run cases that marked as [http]

