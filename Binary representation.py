# --------- Global Variables -----------------

def twos_complement_binary (integer: int) -> str:
	min_binary_bit_len = integer.bit_length() +1
	integer = 2**min_binary_bit_len - integer
	return integer

def convert_to_binary (number: str) -> str:
	negative = False
	binary_integer = ""
	binary_decimal = ""
	try:
		integer_str, decimal_str = str(number).split(".")
	except ValueError:
		integer_str, decimal_str = number, None

#------------------- checking if negative -----------------------
	if '-' in integer_str:
		integer = twos_complement_binary(int(integer_str.strip("-")))
		negative = True
	else:
		integer = int(integer_str)
#-----------------------Decimal----------------------------------------
	if decimal_str is not None:
		decimal_value = float("0." + decimal_str)
		#if negative == True:
			#decimal_value = 1 - decimal_value
		# For two's complement representation of fractional parts, the fractional part of a negative number
		# is represented as (1 - fractional_part), analogous to how the integer part is handled.
		decimal_value = (1-decimal_value) if negative else decimal_value
		while decimal_value > 0:
			decimal_value *= 2
			if decimal_value >=1:
				binary_decimal += "1"
				decimal_value -= 1
			else:
				binary_decimal += "0"

#-----------------------Integer----------------------------------------
	if integer == 0:
		return ("0" if decimal_str is None else ("0", binary_decimal))

	if negative and decimal_str is not None:
		integer -=1 # very important as you "borrow" a negative 1 to "subtract x" to get your desired fractional part 

	while integer > 0:
		remainder = integer % 2
		binary_integer = str(remainder) + binary_integer
		integer = integer // 2

	
	binary_integer = "0" + binary_integer if not negative else binary_integer
	return (binary_integer if decimal_str == None else (binary_integer, binary_decimal))


def binary_to_denary (number: str) -> int:
	decimal_value = 0.0
	integer_value = 0

	try:
		integer_binary , decimal_binary = number.split(".")
		has_decimal = bool(decimal_binary)
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
	
def normalise (binary: str, mantissa_bits: int, exponent_bits: int):
	error = False
	absolute_error = 0
	relative_error = 0
	mantissa = ''.join(binary) #mantissa = binary_integer + binary_decimal
	try:
		binary_integer, binary_decimal = binary # binary_intteger: str, binary_decimal: str

	except ValueError:
		binary_integer = binary

	if binary_integer != '0':
		exponent = len(binary_integer) - 1
		
	else:
		
		k = binary_decimal.find("1")
		exponent = -k
		#mantissa = "0"+binary_decimal[k:] #removing the leading 0s and the first 1

	
	if len(mantissa) > mantissa_bits:
		mantissa_error = mantissa[0]+ "." + mantissa[1:mantissa_bits]
		absolute_error, relative_error = error_calculation (mantissa, mantissa_error, exponent)
		error = True
		mantissa = mantissa[:mantissa_bits]
	
	elif len(mantissa) < mantissa_bits:
		mantissa = mantissa.ljust(mantissa_bits, "0")
	
#------------- Converting the exponent to a binary --------------------
	exponent_binary = convert_to_binary(str(exponent))
	if len(exponent_binary) > exponent_bits and mantissa[0] == "0":
		return "\nExponent bits too small! Overflow error!"
	elif len(exponent_binary) > exponent_bits and mantissa[0] == "1":
		return "\nExponent bits too small! Underflow error!"
	else:
		if exponent_binary[0] == "1": #negative exponent
			exponent_binary = exponent_binary.rjust(exponent_bits,"1")
		else:
			exponent_binary = exponent_binary.rjust(exponent_bits,"0") # Ensuring the exponent binary is in a suitable number of bits available.
	
#------------- Preparing the normliased form --------------------------
	#temp = mantissa[0] + "." + mantissa[1:]
	normalised_form1 = str(binary_to_denary(mantissa[0]+"."+mantissa[1:])) + f"*2^{exponent}"
	normalised_form2 = mantissa + " | " + exponent_binary

	formatting= f"\n\nIn general floating point form: {normalised_form1} / {mantissa[0]}.{mantissa[1:]} *2^{exponent}.\n\nIn full binary form: {normalised_form2[0]}.{normalised_form2[1:]} where {mantissa[0]}.{mantissa[1:]} is your mantissa and {exponent_binary} is your exponent in binary. "
	error_formatting = f"\n\nSince your mantissa bits was too small, we couldn't represent the true value: \nAbsolute error: {absolute_error}\nRelative error: {relative_error}%."

	return (formatting + error_formatting) if error else formatting

def error_calculation (mantissa: str, mantissa_error: str, exponent: int):
	# Calculate the mantissa values in normalized form (0.xxxx)
	full_mantissa_value = binary_to_denary(mantissa[0]+ "." + mantissa[1:])
	truncated_mantissa_value = binary_to_denary(mantissa_error)
	
	# Calculate the actual represented values by applying the exponent
	full_value = full_mantissa_value * (2 ** exponent)
	truncated_value = truncated_mantissa_value * (2 ** exponent)
	
	# Absolute error is the difference in actual values
	absolute_error = full_value - truncated_value
	
	# Relative error uses the full value as denominator
	if full_value == 0:
		relative_error = float('inf')
	else:
		relative_error = (absolute_error / full_value) * 100
	
	return absolute_error, relative_error

def main (number_to_convert , objective, mantissa_bits = None, exponent_bits = None, exponent = None):
	if objective == "d-n": #denary to normalised
		binary = convert_to_binary(number_to_convert)
		normalised_form = normalise (binary, mantissa_bits, exponent_bits)
		return normalised_form
	elif objective == "n-d":
		binary = number_to_convert #binary = mantissa	
		denary = binary_to_denary(number_to_convert)
		return f"\nThe denary value of your normalised binary is: {denary * (2**int(exponent))}"
	
def denary_norm_main():
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
				print(main(user_input, "d-n", mantissa_bits, exponent_bits))
			except ValueError:
				print ("\nHas to be a number.\n")
			
def norm_to_denary_main():
	error = False
	while True:
		user_input = input("\n\n\n Please enter your normalised binary (mantissa only), enter 'exit' to go back to the menu: ")
		if user_input.lower() == "exit":
			break
		
		# Validate using set operations
		if not user_input or not set(user_input).issubset({'0', '1', '.'}):
			print("\n\nHas to be a binary number.")
			continue

		# Check for multiple decimal points
		if user_input.count('.') > 1:
			print("\n\nInvalid format: only one decimal point allowed.")
			continue

		# Ask for exponent type after validation passes
		exponent_type = input("\nHow would you like to enter the exponent?\n[1] Binary\n[2] Integer\nEnter 1 or 2: ")
		
		if exponent_type == "1":
			exponent = input("\nPlease enter your exponent in binary: ")
			try:
				int(exponent, 2)
				exponent = binary_to_denary(exponent)
				error = False
			except ValueError:
				print ("\n\nExponent has to be an integer.\n")
				error = True
		elif exponent_type == "2":
			exponent = input("\nPlease enter your exponent as a integer: ")
			try:
				exponent = int(exponent)
				error = False
			except ValueError:
				print ("\nExponent has to be an integer.")
				error = True
		else:
			print("\nInvalid input. Please try again.")
			continue
		
		if not error:
			print(main(user_input, "n-d", exponent = exponent))
		
def denary_to_binary_main():
	while True:
		user_input = input("\n\nInput a denary number to be converted to binary, enter 'exit' to go back to the menu: ")
	
		if user_input.lower() == "exit":
			break
		try:
			float(user_input)
		except ValueError:
			print ("\n\nHas to be a number.")
			continue
		binary = convert_to_binary(user_input)
		if isinstance(binary, tuple):
			print(f"\nThe binary value of your denary number is: {binary[0]}.{binary[1]}")
		else:
			print(f"\nThe binary value of your denary number is: {binary}")

def binary_to_denary_main():
	while True:
		user_input = input("\n\nInput a binary number to be converted to denary, enter 'exit' to go back to the menu: ")
		if user_input.lower() == "exit":
			break
		
		# Validate using set operations
		if not user_input or not set(user_input).issubset({'0', '1', '.'}):
			print("\n\nHas to be a binary number.")
			continue
		
		# Check for multiple decimal points
		if user_input.count('.') > 1:
			print("\n\nInvalid format: only one decimal point allowed.")
			continue
			
		try:
			denary = binary_to_denary(user_input)
			print(f"\nThe denary value of your binary number is: {denary}")
		except ValueError as e:
			print(e)

def selection():
	while True:
		task = input("""\n\n
Please select one of the following options:
[1] Denary to Normalised Binary
[2] Normalised Binary to Denary
[3] Convert a denary number to binary
[4] Convert a binary number to denary
[5] Exit the program\n\n
Enter 1, 2, 3, 4 or 5 to select: """)
		
		if task == "1":
			denary_norm_main()
		elif task == "2":
			norm_to_denary_main()
		elif task == "3":
			denary_to_binary_main()
		elif task == "4":
			binary_to_denary_main()
		elif task == "5":
			quit = input("\n\nAre you sure you want to quit? (y/n): ")
			if quit.lower() == "y":
				break
		else:
			print ("Invalid input. Please try again.")

if __name__ == "__main__":
	selection()