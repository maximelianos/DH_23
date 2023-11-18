import asyncio
import random
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Health Summary', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')


async def fetch_data_from_ehr1():
    # Simulate network delay
    i = 0
    while i < 3:
        try:
            await asyncio.sleep(random.randint(1, 5))
            if random.randint(1, 100) < 40:
                raise Exception("Network error")
            print("Received data from ehr1")
            return {"name": "Max", "age": 22, "diagnosis": ["flu", "corona"]}
        except Exception as e:
            print(f"ehr1 {e}")
            i += 1
    return None


async def fetch_data_from_ehr2():
    # Simulate network delay
    i = 0
    while i < 3:
        try:
            await asyncio.sleep(random.randint(1, 5))
            if random.randint(1, 100) < 50:
                raise Exception("Network error")
            print("Received data from ehr2")
            return {"name": "Max", "age": 22, "diagnosis": ["cancer", "flu"]}
        except Exception as e:
            print(f"ehr2 {e}")
            i += 1
    return None


async def fetch_data_from_ehr3():
    # Simulate network delay
    i = 0
    while i < 3:
        try:
            await asyncio.sleep(random.randint(1, 5))
            if random.randint(1, 100) < 30:
                raise Exception("Network error")
            print("Received data from ehr3")
            return {"name": "Max", "age": 22, "diagnosis": ["diabetes", "corona"]}
        except Exception as e:
            print(f"ehr3 {e}")
            i += 1
    return None


async def main(pdf):
    ehr1_data, ehr2_data, ehr3_data = await asyncio.gather(fetch_data_from_ehr1(), fetch_data_from_ehr2(),
                                                  fetch_data_from_ehr3())
    summary = []
    per_information = {}

    for dataset in [ehr1_data, ehr2_data, ehr3_data]:
        if dataset is None:
            continue  # skip processing this dataset
        try:
            if not per_information:
                per_information["name"] = dataset["name"]
                per_information["age"] = dataset["age"]
            else:
                if per_information["name"] != dataset["name"]:
                    raise ValueError("Different name")
                if per_information["age"] != dataset["age"]:
                    raise ValueError("Different age")
            for disease in dataset["diagnosis"]:
                if disease not in summary:
                    summary.append(disease)
        except Exception as e:
            print(f"Error: {e}")
            print(dataset["name"])
            print(dataset["age"])

    pdf.cell(0, 10, f"Name: {per_information['name']}", 0, 1)
    pdf.cell(0, 10, f"Age: {per_information['age']}", 0, 1)
    pdf.cell(0, 10, ", ".join(summary), 0, 1)

if __name__ == "__main__":
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    asyncio.run(main(pdf))
    pdf.output('health_summary.pdf')