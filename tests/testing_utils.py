# this is not a test

def assertTrue(someBool):
	if someBool:
		print("PASSED")
	else:
		print("FAILED")
		
def assertFalse(someBool):
	assertTrue(not someBool)
