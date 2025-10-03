# --------- Global Variables -----------------
user_input = ""	

def convert_to_binary (number: str) -> str:
	negative = False
#----------------------Decimal----------------------------------------
	try:
		integer_str, decimal_str = str(number).split(".")
		print(str(number).split("."))
	except ValueError:
		integer_str, decimal_str = number, None
#-----------------------Integer----------------------------------------
	if '-' in integer_str:
		#width = pick_width(int(integer_str))
		integer = int(integer_str.strip("-"))
		min_binary_bit_len = integer.bit_length() +1
		negative = True
	else:
		integer = int(integer_str)
	if decimal_str != None:
		binary_decimal = ""
		decimal_str = "0." + decimal_str
		decimal_value = float(decimal_str)
		if negative == True:
			decimal_value = 1 - decimal_value
		while decimal_value > 0:
			decimal_value *= 2
			if decimal_value >=1:
				binary_decimal += "1"
				decimal_value -= 1
			else:
				binary_decimal += "0"
	if integer == 0:
		return ("0" if decimal_str == None else ("0", binary_decimal))
	if negative:
		integer = 2**min_binary_bit_len - integer
		if decimal_str != None:
			integer -=1 #very important as you "borrow" a negative 1 to "subtract x" to get your desired fractional part 
	binary_integer = ""
	while integer > 0:
		remainder = integer % 2
		binary_integer = str(remainder) + binary_integer
		integer = integer // 2

	if not negative:
		binary_integer = "0" + binary_integer
		 
	#if len(binary_decimal) != width:
		#binary_integer = binary_integer.zfill(width)

	return (binary_integer if decimal_str == None else (binary_integer, binary_decimal))


def binary_to_denary (number: str) -> int:
	decimal_value = 0.0
	integer_value = 0

	try:
		integer_binary , decimal_binary = number.split(".")
		has_decimal = True if decimal_binary != "0" or decimal_binary != "" else False
	except ValueError:
		integer_binary = number
		has_decimal = False

	if has_decimal: #there is a decimal part
		for x in range(len(decimal_binary)):
			if decimal_binary[x] == "1":
				decimal_value += 2**(-x-1) 


	if integer_binary[0] == "1": #negative number
		value = -(2**(len(integer_binary)-1))
		for x in range(1, len(integer_binary)):
			if integer_binary[x] == "1":
				value += 2**(len(integer_binary)-x-1)
		if has_decimal:
			return value + decimal_value
		else:
			return value
	else: #positive number
		for x in range(len(integer_binary)):
			if integer_binary[x] == "1":
				integer_value += 2**(len(integer_binary)-x-1)
		if has_decimal:
			return integer_value + decimal_value
		else:
			return integer_value
	'''if integer_binary != "0":
		for x in range(len(integer_binary)):
			length = len(integer_binary)
			if integer_binary[x] == "1":
				integer_value += 2**(length - x -1)
	
	
	mantissa_value = integer_value + decimal_value
	if integer_binary[0] == "1":
		return -1 * mantissa_value 
	else:
		return mantissa_value'''
	

	
	
def normalise (binary: str, mantissa_bits: int, exponent_bits: int):
	error = False
	mantissa = ''.join(binary) #mantissa = binary_integer + binary_decimal
	try:
		binary_integer, binary_decimal = binary # binary_intteger: str, binary_decimal: str

	except ValueError:
		binary_integer = binary

	if binary_integer != '0':
		exponent = len(binary_integer) if binary_integer[0] != "1" else len(binary_integer[1:])
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
		return "\nExponent bits too small! Overflow error!"
	elif len(exponent_binary) > exponent_bits and mantissa[0] == "1":
		return "\nExponent bits too small! Underflow error!"
	else:
		exponent_binary = exponent_binary.rjust(exponent_bits,"0") # Ensuring the exponent binary is in a suitable number of bits available.
	
#------------- Preparing the normliased form --------------------------
	temp = mantissa[0] + "." + mantissa[1:]
	normalised_form1 = str(binary_to_denary(temp)) + f"*2^{exponent}"
	normalised_form2 = mantissa + " | " + exponent_binary



	return f"\nIn general floating point form: {normalised_form1}.\n\nIn full binary form: {normalised_form2[0]}.{normalised_form2[1:]} where {mantissa[0]}.{mantissa[1:]} is your mantissa and {exponent_binary} is your exponent in binary. "
#def error_calculation ()

def main (number_to_convert , objective, mantissa_bits = None, exponent_bits = None, exponent = None):
	if objective == "d-n": #denary to normalised
		binary = convert_to_binary(number_to_convert)
		normalised_form = normalise (binary, mantissa_bits, exponent_bits)
		return normalised_form
	elif objective == "n-d":
		binary = number_to_convert #binary = mantissa	
		denary = binary_to_denary(number_to_convert)
		return f"\nThe denary value of your normalised binary is: {denary * (2**int(exponent))}"

		


while True:
	task = input("\nWould you like to go from denary to normalised binary (d-n) or normalised binary to denary(n-d)? Please enter 'd-n' or 'n-d' : ")

	if task == "d-n":
		while True:
			user_input = input("\nInput a denary number to be normalised, enter 'exit' to go back to the menu: ")
			if user_input.lower() == "exit":
				break
			mantissa_bits = input("\nEnter the number of bits available for the mantissa: ")
			exponent_bits = input("\nEnter the number of bits available for the exponent: ")
			
			try:
				float(user_input)
				mantissa_bits = int(mantissa_bits)
				exponent_bits = int(exponent_bits)
					#valid = True
			except:
				#valid = False
				raise ValueError ("\nHas to be a number.")
			print(main(user_input, task, mantissa_bits, exponent_bits, None))
	elif task == "n-d":
		while True:
			user_input = input("\nPlease enter your normalised binary (mantissa only), enter 'exit' to go back to the menu: ")
			if user_input.lower() == "exit":
				break
			exponent_type = ""
			while exponent_type != "1" or exponent_type != "2":
				exponent_type = input("\n What type of exponent are you entering?\n [1] binary\n [2] Normal number\n Enter 1 or 2 to select: ")
				if exponent_type == "1":
					exponent = input("\nPlease enter your exponent in binary: ")
					exponent = binary_to_deanery(exponent)
				elif exponent_type == "2":
					exponent = input("\nPlease enter your exponent as a integer: ")
				else:
					print("\nInvalid input. Please try again.")
			print(main(user_input, task, mantissa_bits, exponent_bits, exponent))
	else:
		print ("No")