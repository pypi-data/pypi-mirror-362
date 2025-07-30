import requests

apiUrl = "https://api.shipxy.com/apicall/v3";


def getMethod(methodName, params):
    baseUrl = apiUrl + "/" + methodName
    result = requests.get(baseUrl, params)
    return result


def postMethod(methodName, params):
    baseUrl = apiUrl + "/" + methodName
    result = requests.post(baseUrl, params)
    return result


def getMethodJson(methodName, params):
    baseUrl = apiUrl + "/" + methodName
    result = requests.get(baseUrl, params).json()
    print(result)
    return result


def postMethodJson(methodName, params):
    baseUrl = apiUrl + "/" + methodName
    result = requests.post(baseUrl, params).json()
    print(result)
    return result
