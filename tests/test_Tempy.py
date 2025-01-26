import pytest
class myObj:
    pass

#Fixture is a function that runs before a test case
@pytest.fixture
def Get_Object():
    print("Creating empty object")
    return myObj
class MyExsepshun(Exception):
    pass

@pytest.mark.parametrize("num1,num2,result", [
    (3, 2, 5),
    (7, 5, 12)
])
def test_add(Get_Object,num1, num2, result):
    assert num1 + num2 == result and Get_Object != None

def doRaiseException():
    raise MyExsepshun("Shamalamadingdong")

def test_excepshun():
    #Expects an exception, if no exception is raised, it will complain
    with pytest.raises(Exception):
        doRaiseException()
    