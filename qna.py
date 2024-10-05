import re
from transformers import pipeline

# Load the QA model from Hugging Face
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad", framework="pt")

def clean_context(context):
    # Replace multiple spaces or newline characters with a single space
    cleaned_context = re.sub(r'\s+', ' ', context)
    
    # Replace non-breaking spaces and invisible characters with normal spaces
    cleaned_context = re.sub(r'[^\S\r\n]+', ' ', cleaned_context)
    
    # Strip leading/trailing spaces and return the cleaned context
    return cleaned_context.strip()

# Function to extract shortlisted names using regex
def extract_names(context):
    names_pattern = r"Register No\.\s*Student Name\s*(.*?)\s*(?:Venue Details|Location|Date)"
    names_match = re.search(names_pattern, context, re.DOTALL)
    
    if names_match:
        names_section = names_match.group(1)
        names = re.findall(r"(\d{2}[A-Z]{3}\d{4})\s([A-Za-z\s]+)", names_section)
        clean_names = [name.strip() for _, name in names]
        return ', '.join(clean_names) if clean_names else "No names found"
    
    return "No names found"

# Updated Function to extract the correct date based on context
def extract_when(context):
    # Pattern to capture both date and time, allowing variations in spacing and formats
    when_pattern = r"Date:\s*(\d{1,2}(?:st|nd|rd|th)?\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}).*?Time:\s*([\d:]+\s*(?:AM|PM))"
    when_match = re.search(when_pattern, context, re.DOTALL)
    
    if when_match:
        date = when_match.group(1).strip()
        time = when_match.group(2).strip()
        return f"{date}, {time}"
    
    return "No date or time found"

### 2. Improved Venue Extraction
def extract_venue(context):
    # Refine the regex pattern to capture only the venue and exclude date/time
    venue_pattern = r"Location:\s*(.+?)(?=\s*(?:Date|Time|Map:|\Z))"  # Stops matching when it encounters 'Date', 'Time', or 'Map:'
    venue_match = re.search(venue_pattern, context, re.DOTALL)
    
    # Clean and return the venue information
    if venue_match:
        full_venue = venue_match.group(1).strip()  # Strip any extra leading/trailing spaces
        if full_venue:
            return ' '.join(full_venue.split())  # Replace multiple spaces/newlines with a single space for readability
    return "No venue found"

# Function to extract tasks/labs to be completed
def extract_tasks(context):
    task_pattern = r"Lab\s*\d+|Contest\s*\d+"
    tasks = re.findall(task_pattern, context)
    return ', '.join(tasks) if tasks else "No tasks found"

# Generalized function to get the answer using QA model as fallback
def get_answer(context, question, use_regex=True):
    # Clean the context first
    context = clean_context(context)
    
    # Use regex for specific types of questions
    if "shortlisted" in question.lower() and use_regex:
        return extract_names(context)
    elif "date" in question.lower() or "when" in question.lower() and use_regex:
        return extract_when(context)
    
    # Check for keywords like "venue", "location", or "where" to extract the venue
    elif any(keyword in question.lower() for keyword in ["venue", "location", "where"]):
        return extract_venue(context)
    
    # Check for task-related questions
    elif "complete" in question.lower() or "tasks" in question.lower():
        return extract_tasks(context)
    
    # Fallback to the QA model for general questions
    result = qa_pipeline({'context': context, 'question': question})
    return result['answer']


# Sample email context
context = """
6. SenderName: "'Helpdesk CDC' via B.Tech. - Comp Sci Engg 2022 Group, Vellore Campus"|Date & Time: Fri, 4 Oct 2024 10:24:54 +0530|Subject: KLA Next round of selection process is scheduled on (11th October 2024) at 8:30 am - (KLA) Chennai office|SenderEmail: 22bce@vitstudent.ac.in|Text: KLA Next round of selection process is scheduled on ( 11th October 2024) at 8:30 am - ( KLA ) Chennai office Please find the below shortlisted students list. Register No. Student Name 22BCE5238 Sinchan Shetty 22BAI1470 Modupalli Lasya 22BCE3488 Daksha Bhusnur 22BCE0756 Apoorva Karnwal 22BCE3943 Nandini Chaurasia 22BCE3953 Mudita Bhathar 22BCE0602 Vanshika Agrawal Venue Details: Date: 11 th O ctober 2024, F riday Time: 08:30 AM Location: 5th Floor, Campus-4b, RMZ MILLENIA BUSINESS PARK-II, Kodandarama Nagar, Perungudi, Chennai, Tamil Nadu 600096 Map: https://maps.app.goo.gl/y97e1QkFopDPkYNg8 T he above shortlisted candidate is informed to plan their travel accordingly on their own and report in KLA - Chennai office sharply by 08:30 AM Note: Candidate failed to attend the scheduled interview process in KLA - Chennai office will be blacklisted from further placements. Note : 1. Students are requested to send their queries to their respective campus email ID only. 2. Webcam Should be turned on till the test gets over Important Note: 1. Appear for the selection process in formal dress. 2. Carry your 2 sets updated Resumes & pens , photos, College photo ID and all other relevant certificates... (Photo Copy of Mark Sheets - PG, UG,  Higher Secondary 10th) 3.Latecomers will not be allowed to attend the selection process . -- Warm regards Dr.V.Samuel Rajkumar, B.E.,MBA, MHRM, PhD Director(Career Development Centre) VIT, Vellore -14
"""

# Example questions to ask
question_1 = "Who all are shortlisted for KLA?"
question_2 = "When is  the next round selection process?"
question_3 = "What is the location for the next round of Selection process?"

# Get answers to the questions using regex first, and fallback to QA if necessary
answer_1 = get_answer(context, question_1)
answer_2 = get_answer(context, question_2)
answer_3 = get_answer(context, question_3)

# Display the answers
print(f"Answer 1: {answer_1}")
print(f"Answer 2: {answer_2}")
print(f"Answer 3: {answer_3}")
