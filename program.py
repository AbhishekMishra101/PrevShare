class Program:
    def __init__(self):
        pass

    def collect_data(self, file_path):
        # Placeholder for collecting patient data from the uploaded file
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Process each patient record
                    self.process_patient_record(row)
                print("Patient data collected successfully.")
        except Exception as e:
            print("Error:", e)

    def process_patient_record(self, record):
        # Process each attribute of the patient record
        print("Name:", record['Name'])
        print("Age:", record['Age'])
        print("Gender:", record['Gender'])
        print("Blood Type:", record['Blood Type'])
        print("Medical Condition:", record['Medical Condition'])
        print("Date of Admission:", record['Date of Admission'])
        print("Doctor:", record['Doctor'])
        print("Hospital:", record['Hospital'])
        print("Insurance Provider:", record['Insurance Provider'])
        print("Billing Amount:", record['Billing Amount'])
        print("Room Number:", record['Room Number'])
        print("Admission Type:", record['Admission Type'])
        print("Discharge Date:", record['Discharge Date'])
        print("Medication:", record['Medication'])
        print("Test Results:", record['Test Results'])
        print()
        
    def apply_differential_privacy(self, record):
        # Apply differential privacy to numeric attributes (e.g., age, billing amount)
        numeric_attributes = ['Age', 'Billing Amount']
        for attr in numeric_attributes:
            if attr in record:
                # Calculate sensitivity (maximum change in attribute value)
                sensitivity = 1.0  # Adjust as needed based on the attribute range and query function

                # Generate Laplace noise
                noise = random.gauss(0, sensitivity / self.epsilon)

                # Add noise to the attribute value
                perturbed_value = float(record[attr]) + noise

                # Update the record with the perturbed value
                record[attr] = perturbed_value
                
    def generate_perturbed_data(self, original_data):
        perturbed_data = []
        for record in original_data:
            perturbed_record = dict(record)  # Create a copy of the original record

            # Apply perturbation to numeric attributes
            perturbed_record['Age'] += random.randint(-5, 5)  # Example: Add random noise to age
            perturbed_record['Billing Amount'] += random.uniform(-50, 50)  # Example: Add random noise to billing amount

            # Apply perturbation to categorical attributes
            # Example: Add random noise to gender (with 5% probability)
            if random.random() < 0.05:
                perturbed_record['Gender'] = random.choice(['Male', 'Female'])

            # Apply perturbation to other attributes as needed

            perturbed_data.append(perturbed_record)

        return perturbed_data
    
    

def main():
    program = Program()
    file_path = "hospital_patient_data.csv"  # Replace with the path to your CSV file
    program.collect_data(file_path)

    # Generate perturbed data
    perturbed_data = generate_perturbed_data()

    # Store and share perturbed data
    program.store_perturbed_data(perturbed_data)
    program.share_perturbed_data(perturbed_data)

if __name__ == "__main__":
    main()
