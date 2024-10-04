from transformers import pipeline

# Initialize the question-answering pipeline
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
context="""3. SenderName: 'Dr.R.Seenivasan Director (IR)' via B.Tech. - Comp Sci Engg 2022 Group, Vellore Campus"|Date & Time: Fri, 4 Oct 2024 12:35:48 +0530|Subject: Meeting today at 2 pm Reminder : Great Opportunity for scholarships ..fee waivers by Binghamton University USA and more ...also o interact with the Dean and Vice Provost -SUNY-BU USA-Orientation Session on International Transfer programs to Binghamton University, USA: reg|SenderEmail: 22bce@vitstudent.ac.in|Text: Reminder On Thu, 3 Oct, 2024, 10:05 Dr.R.Seenivasan Director (IR), < director.ir@vit.ac.in > wrote: Kind Attn: Only for 2nd year BTech, 4th Year BTech: Reg Dear Students This is to inform you that the IR office is organizing an orientation session on 2+2 and 3.5+1.5 International Transfer programs to Binghamton University, USA for BTech 2nd Year and BTech 4th Year Program respectively. Interested students can join the session on 4th Oct'24 at 2:00 PM in the Smart Classroom 304 CDMM block. Great Opportunity to meet with the Dean  and Vice Provost -SUNY-BU USA Dr Atul Kelkar Dean of Thomas J. Watson College of Engineering and Applied Science Dr.Madhusudhan Govindaraju Vice Provost for International Education and Global Affairs (IEGA); Professor, School of Computing State University of New York at Binghamton, USA Best Regards, R Seenivasan Disclaimer: This message was sent from Vellore Institute of Technology.  The contents of this email may contain legally protected confidential or privileged information of “Vellore Institute of Technology”.  If you are not the intended recipient, you should not disseminate, distribute or copy this e-mail. Please notify the sender immediately and destroy all copies of this message and any attachments. If you have received this email in error, please promptly notify the sender by reply email and delete the original email and any backup copies without reading them."""
question="When is the orientation session on 2+2 and 3.5+1.5 International Transfer programs to Binghamton University "
# Get the answer from the model
def get_answer(context, query):
    result = qa_pipeline({
        'context': context,
        'question': query
    })
    return result['answer']
print(get_answer(context,question))
