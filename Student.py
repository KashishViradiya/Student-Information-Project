# Google Sheet ID and sheet name
sheet_id = "1hl3uC3BmTu7GNFF_ixkCuqn4apPNcVdOA53htNwZDIY"
sheet_name = "AllStudents"

# Mapping of output types to column names
output_types = {
    "enrollment number": "Enrollment No.",
    "mobile number": "Student Phone No",
    "class": "Class",
    "email id": "Student gnu mail Id",
    "semester": "Semester",
    "batch": "Batch"
}

# Function to fetch student data from the Google Sheet
def get_student_data(first_name, last_name=None, output_type=None):
    if last_name:
        student_name = f"{last_name} {first_name}"
    else:
        student_name = first_name
    url = f"https://script.google.com/macros/s/AKfycbwP3XOlI33GcQzZ1m7DWzt-CuwRy3YB8BBwGU_0lFf7KD56kUY/exec?spreadsheet=a&action=getbyname&id={sheet_id}&sheet={sheet_name}&sheetuser={student_name}&sheetuserIndex=2"
    response = requests.get(url)
    data = response.json()

    if isinstance(data, dict) and 'records' in data:
        return data['records']
    else:
        return None  # Handle invalid API response format

# Function to extract information from the Alexa request
def extract_information(request):
    slots = request['intent']['slots']
    first_name = slots.get('FirstName', {}).get('value')
    last_name = slots.get('LastName', {}).get('value')
    output_type = slots.get('OutputType', {}).get('value')

    return {"first_name": first_name, "last_name": last_name}, output_type


class GetStudentInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetStudentInfoIntent")(handler_input)

    def handle(self, handler_input):
        request = handler_input.request_envelope.request
        name, output_type = extract_information(request)
        
        if not name or not output_type:
            speak_output = "Could not extract information from the request. Please try again."
        else:
            first_name = name.get("first_name")
            last_name = name.get("last_name")
            student_data = get_student_data(first_name, last_name, output_type)

            if not student_data:
                speak_output = f"No data found for {first_name} {last_name}."
            else:
                if len(student_data) == 1:
                    speak_output = f"The {output_type} is: {student_data[0][output_types[output_type]]}"
                else:
                    speak_output = f"Multiple records found for {first_name} {last_name}."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )