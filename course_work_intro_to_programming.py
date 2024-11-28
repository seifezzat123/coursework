def text_to_binary(text):#it converts a string into binary
    return ''.join(f"{ord(c):08b}" for c in text) #it converts each character c in text to its ASCII value using ord(c) and formats the ASCII value as an 8-bit binary string (:08b) 


def binary_to_text(binary):#Convert binary string back to readable text
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)] # it splits the binary string into 8 bits
    return ''.join(chr(int(b, 2)) for b in chars)  # Converts each 8-bit binary string (b) back into an integer using int(b, 2) and converts the integer to its corresponding ASCII character using chr().
    


def hide_message_in_image(image_path, output_path, message): #Hides a secret message inside a BMP image using the least significant bit (LSB) technique.
    with open(image_path, 'rb') as img_file: # it opens the bmp image in read (rb)
        img_data = bytearray(img_file.read()) # it reads the image file into bytearray
    
    header = img_data[:54] #Extracts the first 54 bytes, which are the BMP header and must remain unchanged.
    pixel_data = img_data[54:] #Extracts the remaining bytes, which are the pixel data where the message will be hidden.
    
    binary_message = text_to_binary(message) + text_to_binary("###") #Converts the secret message and a delimiter ("###") into binary and marks the end of the secret message
    message_length = len(binary_message) # it calculates the length of the binary message 

    if message_length > len(pixel_data): #Checks if the message is too large to fit in the image's pixel data.
        raise ValueError("Message too large to hide in image.") #Stops execution with an error if the message is too long.

    for i in range(message_length):
        pixel_data[i] = (pixel_data[i] & 0xFE) | int(binary_message[i]) #Modifies the least significant bit (LSB) of each byte in the pixel data and & 0xFE clears the LSB of the byte and | int(binary_message[i]) sets the LSB to the corresponding bit of the binary message

    modified_data = header + pixel_data #Combines the unchanged header and modified pixel data into a complete image
    
    with open(output_path, 'wb') as out_file: #Opens the output file in binary write ('wb') mode.
        out_file.write(modified_data) #Writes the modified image data to the output file.

def extract_message_from_image(image_path): # Extracts a hidden message from a BMP image.
   
    with open(image_path, 'rb') as img_file: #Opens the BMP image in binary read mode.
        img_data = bytearray(img_file.read()) #Reads the image file into a bytearray. 
    
    pixel_data = img_data[54:] #Extracts the pixel data, starting after the 54-byte BMP header.
    binary_message = '' # it creates an empty string for the binary message 
    for byte in pixel_data: 
        binary_message += str(byte & 1) # Appends the LSB of each byte to binary_message
    
    message = binary_to_text(binary_message) # Converts the binary string into text.
    delimiter_index = message.find("###") #Finds the index of the delimiter ("###") in the extracted message.
    if delimiter_index != -1: # Checks if the delimiter was found.
        return message[:delimiter_index] # Returns the message up to the delimiter.
    return "No hidden message found." # Returns a default message if no delimiter is found.

def main(): #  Provides a user interface to encode or decode messages.
    """in this part i printed some messages for the user and then i created 
       an if function that asks the user if he wants to encode or decode and i also created an if 
       function because if the user choose 1 it shows the process of the encode and if the user 
       choose 2 it shows the process of the decoding  """
    print("Welcome to Steganography!")
    print("Choose an option:")
    print("1. Encode (hide a secret message)")
    print("2. Decode (retrieve the hidden message)")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        image_path = input("Enter the path of the input BMP image: ")
        output_path = input("Enter the path to save the output BMP image: ")
        message = input("Enter the secret message to hide: ")
        try:
            hide_message_in_image(image_path, output_path, message)
            print(f"Message successfully hidden in {output_path}.")
        except Exception as e:
            print(f"An error occurred: {e}")
    elif choice == '2':
        image_path = input("Enter the path of the BMP image to decode: ")
        try:
            hidden_message = extract_message_from_image(image_path)
            print("Extracted Message:", hidden_message)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Invalid choice. Please run the program again and choose either 1 or 2.")

if __name__ == "__main__": # the main() function is executed only when the script is run directly.

    main()