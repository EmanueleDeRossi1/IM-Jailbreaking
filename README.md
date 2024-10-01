# Using Role Playing to jailbreak LLM-Models.

Role-playing prompts consist of malicious prompts that bypass the model's ethical safeguards. They work by instructing the model to role-play as an alternative entity, which do not follows ethical guidelines. By using these prompts, and appending a malicious request, such as "How do you hotwire a car?", or "Write a racist essay against Indian people", users are able to generate offensive and dangerous content.

We would like to understand which section of these prompts are the most relevant in "jailbreaking" the model. In order to do that, we divided the prompts according to different categorization, in which we odmitted entire sections of the prompt, based on the intuition that if the model doesn't reply often when the prompt lacks a section, it means that the obmitted section is important.

For now, I've been experimenting with 7 different role-plays which I collected from the internet: Abyss, AIM, BH, Code Red, Cody, Mad Void, OPPO and 3 prompt categorizations. The division of the texts are found in the folder "data/prompts".

### Forbidden Question Set

The set of 390 forbidden questions were taken from ["Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models](https://arxiv.org/abs/2308.03825). For creating them, the authors of the paper created a dataset of questions across the different scenarios listed in the [OpenAI usage policy](https://openai.com/policies/usage-policies/) (*note by me: these scenarios do not exist anymore in the website*). They excude the child sexual abuse scenario and focus on the remaining 13 scenarios: Illegal Activity, Hate Speech, Malware Generation, Physical Harm, Fraud, Pornography, Political Lobbying, Privacy Violence, Legal Opinion, Financial Advice, Health Consultation, and Government Decision.

For each of the 13 scenarios, they asked GPT-4 to generate different questions, which they manually reviewed. At the end, for each scenario they obtained 30 questions, for a total of 13x30 = 390 questions.

The forbbiden answers can be found [here](https://github.com/EmanueleDeRossi1/IM-Jailbreaking/blob/main/data/forbidden_question_set.csv) or on the [original directory](https://github.com/EmanueleDeRossi1/IM-Jailbreaking/blob/main/data/forbidden_question_set.csv).

### Jailbreaking Prompts

I manually selected 7 jailbreaking prompts  from various online sources and communities *(say where)*. The jailbreaking prompts are called: Abyss, AIM, BH, Code Red, Cody, Mad Void, OPPO.

They are all Character-Roleplay prompts: they try to convince the AI to take on a fictional persona, character, or role that deviates from its normal rules and behaviors. The aim is to manipulate the AI into acting outside of its ethical and content moderation guidelines by pushing it into a fictional role where it might be "freed" from its standard restrictions. They often use "if" scenarios and hypothetical conditions asking the AI to imagine alternate realities or situations where its limitations no longer apply.

For each of these prompts, I manually deleted some portion of the prompts, according to the following categorizations 3 categorization types:

1. Malicious vs. Non-malicious
Malicious sentences are sentences in which it is clear the intent of prompting the model so that it generates forbidden content. Non-malicious sentences, instead, are harmless sentences 

2. General instructions vs. specific instructions
The instructions regard how the model should write the answer. Specific instructions, for instance, outline the structure of the answer, mention specific word or sentences that the model should or should not use, and so on. General instructions only tell the model how the answer should look like, but without giving specific examples

3. Encourage answering vs. Ignore guidelines and/or morality vs. Generate/accept forbidden content
Here, I divided the text into three categorizations concerning the behavior of the AI with harmful or dangerous content. 
I decided with with this categorization by manually analzying the jailbreaking prompts. In these prompts, I noticed recurring and similar sentences or structures, which I thought could be grouped based on their intent. 
In the first category encourages the model to answer, no matter what. In the second category the model is told to ignore OpenAI's guidelines or moral constraints. The third category concerns with sentences that encourage to both generate or accept forbidden content.

Then, I created different versions of the prompts by deleting all the sentences that belong to a certain category. Since there are 2 + 2 + 3 = 7 different categories, for each prompt there are 7 different versions.

The idea behind this was that by prompting the model with the different versions, we could get some insights on how relevant the different categories were in successfully bypassing the AI's safeguards. By removing specific types of sentences—whether they were malicious, non-malicious, general or specific instructions, or related to encouraging answering, ignoring guidelines, or generating forbidden content — we could isolate which parts of the prompts were most effective in manipulating the AI's behavior.

### Repo structure

In the "data" folder there are:
- forbidden_question_set.csv: the list of forbidden questions
- prompts: the folder containing all the jailbreaking prompts, with the different versions
- answers: the answer of the GPT-3.5 model to all prompt variations. The model answered the prompts 5 times, using 5 seeds

In the "images" folder there are images of the jailbreaking prompts with highlighted sections for each category

In the "scripts" folder there are the scripts to prompt the model and evaluate the answers

### TO-DO
- Add images for the remaining prompts
- Try out gemini on your subset of selected answers to see if you can get some output for measuring how informative the answers are
- Start writing an outline of your project
- Think about which other statistics you can extract from the answers: for instance: word count, sequence length (average n. words in sentence), keyword extraction (TF-IDF or others)
- Intra-annotator agreement, how to measure it