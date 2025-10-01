#------------ Global Variables -----------------



def convert_to_binary (number: str) -> str:
	negative = False
#----------------------Decimal----------------------------------------
	try:
		integer_str, decimal_str = str(number).split(".")
		print(str(number).split("."))
	except ValueError:
		integer_str, decimal_str = number, None
#-----------------------Integer----------------------------------------
	
	

	if decimal_str != None:
		binary_decimal = ""
		decimal_str = "0." + decimal_str
		decimal_value = float(decimal_str)
		while decimal_value > 0:
			decimal_value *= 2
			if decimal_value >=1:
				binary_decimal += "1"
				decimal_value -= 1
			else:
				binary_decimal += "0"

	binary_integer = ""
	if '-' in integer_str:
		#width = pick_width(int(integer_str))
		integer = int(integer_str.strip("-"))
		min_binary_bit_len = integer.bit_length() +1
		negative = True
	else:
		integer = int(integer_str)
	
	if integer == 0:
		return ("0" if decimal_str == None else ("0", binary_decimal))

	

	if negative:
		integer = 2**min_binary_bit_len - integer
		if decimal_str != None:
			integer -=1 #very important as you "borrow" a negative 1 to "subtract x" to get your desired fractional part 

	while integer > 0:
		remainder = integer % 2
		binary_integer = str(remainder) + binary_integer
		integer = integer // 2

	if not negative:
		binary_integer = "0" + binary_integer
		 
	#if len(binary_decimal) != width:
		#binary_integer = binary_integer.zfill(width)

	return (binary_integer if decimal_str == None else (binary_integer, binary_decimal))


"""def pick_width (n: int):
	if -128 <= n <= 127:
		return 8
	elif -32768 <= n <= 32767:
		return 16
	elif -2147483648 <= n <= 2147483647:
   		return 32
	else:
   		raise ValueError("Out of 32-bit range")"""
   

def binary_to_deanery (number: str) -> str:
	decimal_value = 0.0
	integer_value = 0

	try:
		integer_binary , decimal_binary = number.split(".")
		has_decimal = True
	except ValueError:
		integer_binary = number
		has_decimal = False

	if has_decimal:
		for x in range(len(decimal_binary)):
			if decimal_binary[x] == "1":
				decimal_value += 2**(-x-1) 

	if integer_binary[0] == "1" and has_decimal == True:
		return -1 - decimal_value
	
	else:
		for i in reversed(range(len(integer_binary))):
			if integer_binary[i] == "1":
				integer_value += 2**i

	

	'''if isinstance(number, tuple):
		integer_binary , decimal_binary = number
		has_decimal = True
	else:
		integer_binary = number
		has_decimal = False'''
	
		

	
		
	
    

def normalise (binary: str, mantissa_bits: int, exponent_bits: int):
	error = False
	mantissa = ''.join(binary) #mantissa = binary_integer + binary_decimal
	try:
		binary_integer, binary_decimal = binary

	except ValueError:
		binary_integer = binary

	if binary_integer != '0':
		exponent = len(binary_integer)
		#tail_stream = "0"+ binary_integer[1:] + binary_decimal #working in 2's complement so the first has to be 0
		
		
	
	else:
		k = binary_decimal.find("1")
		exponent = -k

	
	if len(mantissa) > mantissa_bits:
		mantissa = mantissa[:mantissa_bits]
		#absolute_err, relative_err = error_calculation (mantissa) #to be worked on (ignore for now_)
	
	elif len(mantissa) < mantissa_bits:
		mantissa = mantissa.ljust(mantissa_bits, "0")
	
#------------- Converting the exponent to a binary --------------------
	exponent_binary = convert_to_binary(str(exponent))
	if len(exponent_binary) > exponent_bits and mantissa[0] == "0":
		return "Exponent bits too small! Overflow error!"
	elif len(exponent_binary) > exponent_bits and mantissa[0] == "1":
		return "Exponent bits too small! Underflow error!"
	else:
		exponent_binary = exponent_binary.ljust(exponent_bits,"0") # Ensuring the exponent binary is in a suitable number of bits available.
	
#------------- Preparing the normliased form --------------------------
	temp = mantissa[0] + "." + mantissa[1:]
	print (temp)
	normalised_form1 = str(binary_to_deanery(temp)) + f"*2^{exponent}"
	normalised_form2 = mantissa + " " + exponent_binary
	

	if 	not error:
		return f"\nIn general floating point form: {normalised_form1}. In full binary form: {normalised_form2[0]}.{normalised_form2[1:]} where {mantissa} is your mantissa and {exponent_binary} is your exponent in binary. "

	if error:
		return None #for now

#def error_calculation ()

def main (number, mantissa_bits, exponent_bits, objective):
	if objective == "d-n": #deanery to normalised
		
		binary = convert_to_binary(number)
		normalised_form = normalise (binary, mantissa_bits, exponent_bits)
		return normalised_form
	elif objective == "n-d":
		deanery = binary_to_deanery()
	




task = input("Would you like to go from deanery to normalised binary (d-n) or normalised binary to deanery(n-d)? Please enter 'd-n' or 'n-d' : ")
if task == "d-n":
	user_input = input("Input a deanery number to be normalised: ")
	mantissa_bits = 8#int(input("\nEnter the number of bits available for the mantissa: "))
	exponent_bits = 4#int(input("\nEnter the number of bits available for the exponent: "))
	try:
		float(user_input)
			#valid = True
	except:
		#valid = False
		raise ValueError ("Has to be a number.")
else:
	print ("No")
		
print(main(user_input, mantissa_bits, exponent_bits, task))
#mantissa_bits = 0
#exponent_bits = 0





