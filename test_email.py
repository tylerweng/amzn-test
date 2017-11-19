import boto3
import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(10, 4), columns=['A', 'B', 'C', 'D']) * 10000

def email(bodytext = 'No data...check your function arguments', dftoconvert = None, replace=False):
    region = 'us-west-2'
    user = '' #insert your access key to use when creating the client
    pw = '' #insert the secret key to use when creating the client
    client = boto3.client(service_name = 'ses',
                          region_name = region,
                          aws_access_key_id = user,
                          aws_secret_access_key = pw)
    me = 'me@example.com'
    you = ['you@example.com']
    subject = 'testSUBJECT'
    COMMASPACE = ', '
    you = COMMASPACE.join(you)
    #Build email message parts

    #Build and send email
    destination = { 'ToAddresses' : [you],
                    'CcAddresses' : [],
                    'BccAddresses' : []}
    try:
        bodyhtml = dftoconvert.to_html(float_format = lambda x: '({:15,.2f})'.format(abs(x)) if x < 0 else '+{:15,.2f}+'.format(abs(x)))
        # use no-break space instead of two spaces next to each other
        if replace:
            bodyhtml = bodyhtml.replace('  ', '&nbsp;')
        message = {'Subject' : {'Data' : subject},
                   'Body': {'Html' : {'Data' : bodyhtml}}}
    except NoneType: #If there is no data to convert to html
        message = {'Subject' : {'Data' : subject},
                   'Body': {'Text' : {'Data' : bodytext}}}
    except Exception as e:
        print(e)
    result = client.send_email(Source = me,
                               Destination = destination,
                               Message = message)
    return result if 'ErrorResponse' in result else ''

email(dftoconvert=df)
email(dftoconvert=df, replace=True)
