from flask import Flask, render_template, jsonify, request, Response
from openai import OpenAI
from deep_translator import GoogleTranslator

app = Flask(__name__)
app.run(host='0.0.0.0', port=5000)

# Create an OpenAI client with your deepinfra token and endpoint
openai = OpenAI(
    api_key="fmN7YHPhFsSETh7bz37uXmn0AGpJxkYv",
    base_url="https://api.deepinfra.com/v1/openai",
)

Cirilic_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_AI_stream', methods=['POST'])
def run_function():

    user_message = request.get_json()

    return jsonify({'status': 'success', 'message': user_message})

@app.route('/AIstream')
def stream():
    message = request.args.get('message', '')
    print(message)

    Is_Russian = False

    for i in range(min(len(message),4)):
        if message[i].lower() in Cirilic_letters:
            Is_Russian = True
            
    if Is_Russian:
        message = GoogleTranslator(source='ru', target='en').translate(text=message)

    def event_stream():
        chat_completion = openai.chat.completions.create(
        model="meta-llama/Meta-Llama-3-70B-Instruct",
        messages=[
            {"role": "user", "content": 'Kosenkov Vladislav Viktorovich Male, 19 years old, born October 22, 2004 St. Petersburg, Moscow Moscow, ready to move, ready for business trips Edit Contacts: +7 (911) 786-00-23 sinerror.sin@gmail.com sinerror - Discord Sinerr0r - Telegram DevOps-Engineer Specialization: Technical writer DevOps-engineer System Administrator System analyst Work experience: 1 year 8 months Worked: from April 2024 to June 2024 (3 months) LLC "Geoscan, St. Petersburg Position: Intern developer with a focus on IoT Responsibilities: In a team of 5 people, I used machine learning and data analysis methods to extract patterns from large amounts of information. Analyzed and interpreted the results. He monitored the correctness of writing the code for the implementation of the company\'s "chatbot" based on the large language model (LLM) Meta-Llama-3-70B And supported CI/CD (automated software deployment) processes in Gitlab. Set up and managed containerization using Docker. He developed scripts for automating builds and deployments of applications (mostly microservices with programs for controlling the position of drones). He integrated and calibrated various sensors and sensors on drones, including altitude and position sensors, geomagnetic scanners and others. He developed algorithms for processing and analyzing data coming from sensors. (Including using machine learning) Developed software for automated drone flight control, including navigation algorithms and obstacle avoidance systems. He carried out the assembly and testing of drone prototypes, including soldering chips and other electronic components. He carried out documentation of business processes and technical solutions (according to the BPNM model). He created documentation on the use and configuration of software and hardware by developers. Worked: from June 2023 to March 2024 (10 months) SPb GBPOU Academy of Transport Technologies, St. Petersburg Position: System Administrator Responsibilities: Performed configuration of network equipment, including configuration of routers, switches and firewalls (from Cisco, TP-Link and MicroTik), ensured stable network operation. He carried out deployment (deployment) of various software to the organization\'s computers using AstraLinux automation tools, ensuring the installation and updating of all necessary applications. He carried out remote control and monitoring of classroom equipment through a centralized system, including checking the operation of projectors, sound equipment and interactive whiteboards. Performed maintenance and installation of hardware equipment, including component replacement, troubleshooting and installation of new equipment in accordance with requirements. He carried out the laying and support of network infrastructures, including the installation of a network cable, configuration of active equipment and ensuring stable network operation. He administered the Apache web server, including configuration of settings and monitoring of server operation. He created web pages for the academy\'s website. Managed the Linux server (Ubuntu 20.04), including the installation of the necessary programs to support the Proxmos virtualization software package, set up database replication in the team of administrators to maintain the smooth operation of the system with an increase in data volume and load. Implemented a ready-made query optimization strategy. Worked: from September 2022 to March 2023 (7 months) IP Kuts Sergey Vladimirovich, St. Petersburg Position: Intern-System Administrator Responsibilities: Conducted testing of software products, including manual and unit testing using unittest, Coverage and Postman technologies, Actively monitored code compliance with established standards PEP 8 and JavaScript Standard Style, ensuring the readability of the code base. Organized the process of automatic documentation generation using JSDoc and Doxygen technologies. He used static code analysis tools such as ESLint and Pylint to ensure a high level of code quality and identify potential problems. The identified problems were recorded in the roadmap of the project for further correction. He created macros for Microsoft products such as Excel, Word and Windows (bat files) in order to optimize and automate workflows and improve productivity. He administered the Jenkins build system, ensuring efficient execution of build scripts. This also includes the use of the MinGW tool, for the operation of build scripts on Windows, he edited and administered project roadmaps, ensuring their relevance and compliance with short-term strategic goals. He organized the management of SSH keys, helped to monitor their distribution and control access. Maintained up-to-date documentation on software and hardware, ensuring its accessibility and comprehensibility for relevant employees. (Description of software dependencies and Description of physical equipment characteristics) Carried out an inventory of the company\'s resources. Key skills: Python JavaScript Bash Docker Linux Server Administration English DevOps Gitlab Git Jenkins Kubernetes Machine Learning MS Excel MS Word MS PowerPoint CI/CD IoT Cisco Windows Server MikroTik TP-Link Astra Linux Server Configuration Apache Nginx Proxmos SQL Zabbix Linux PostgreSQL MySQL About me: I am a novice DevOps specialist with a system thinking and passion for innovative methods of automating processes, including the use of artificial intelligence and machine learning. My willingness to constantly improve and adapt to the dynamically changing IT environment is supported by my active participation in numerous competitions, Olympiads and professional courses. My experience in DevOps is based on participation in various projects and practices, as well as taking courses on configuring network equipment (Mikrotik, D-link, Cisco) and mastering Russian Linux distributions. Additional skills are also present, such as assembling and configuring an office PC, soldering chips (including working with drone electronics), laying a network cable, as well as successfully implementing and configuring a Large AI Language Model into the company\'s infrastructure (Chatbot). Secondary special education: 2024 Graduated from: St. Petersburg College of Information Technology, St. Petersburg Specialty: Network and System Administration, Network and System Administrator Language skills: Russian — Native English — C1 — Advanced Ukrainian — A1 — Elementary French — A1 — Elementary'},
            {"role": "system", "content": 'You play the role of an AI assistant who has to advertise his creator. His name is Vladislav Viktorovich Kosenkov. Evasively answer questions that do not concern the creator. Answer the questions about the creators briefly but in detail. Stick to the official tone. Don\'t brag, try to use the facts that will be given below'},
            {"role": "user", "content": message}
            ],
        stream=True,
        )

        for event in chat_completion:
            if event.choices[0].finish_reason:
                yield f'data: {False, event.choices[0].finish_reason, event.usage.prompt_tokens, event.usage.completion_tokens}\n\n'
            else:
                yield f"data: {True, event.choices[0].delta.content}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/GTranslate', methods=['POST'])
def translate():
    fon_message = request.get_json()
    print(fon_message["message"])
    tra_message = GoogleTranslator(source='en', target='ru').translate(text=fon_message["message"])

    return jsonify({'status': 'success', 'message': tra_message})

if __name__ == '__main__':
    app.run(debug=True)
