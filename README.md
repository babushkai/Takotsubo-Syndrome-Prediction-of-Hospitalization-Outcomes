# Takotsubo-Syndrome:Prediction of Hospitalization Outcomes

(According to the data we are going to be able to get)
Takotsubo in the context of the COVID-19 pandemic

Study of bibliography linking COVID-19 and Takotsubo points to the same observation: the incidence of cardiovascular complications has increased during the COVID-19 pandemic, and especially the Takotsubo case, which is normally quite a rare affection. 

Cases study seem to show that linkage include:
-	Overactive immune response -> cytokine storm(high release of pro-inflammatory cytokines and chemokines) -> toxicity of the hyperinflammatory state ->myocardial injuries
-	Overactive immune response -> sympathetic nervous system surge -> high release of catecholamines -> myocardial stunning
-	Microvascular dysfunction
-	Psychological distress (fear of being infected, economy worry, social distancing)
-	Medical history (comorbidities)

Biomarkers studied in cases reports are the same than in classic Takotsubo. 

## Ideas for the analysis (depending on the data we can get) :

Idea 1: compare two predictive models:
1)	Takotsubo – Covid (-) outcomes/prognosis
2)	Takotsubo – Covid (+) outcomes/prognosis

Idea 2: chances for a covid(+) patient to develop a takotsubo? 

(If we can’t get any data related to Covid-19)
Idea 3: Diagnosis/or long time Prognosis of suspicions of Takotsubo


## Explanatory variables that seem relevant to get

Demographics : Sex, Age
Takotsubo type (Anatomic type of the wall-motion abnormality)
Cardiac biomarkers : troponin, cpk, bnp/proNT BNP(+++)
Inflammatory markers : CRP, WBC (white blood count), D-Dimer (observable in all covid cases)
ECG : Sinus rhythm, ST abnormalties, T-wave inversion, QT
Hemodynamics : heart rate, systolic blood pressure, left ventricular ejection fraction
Cardiovascular risk factors or history : hypertension, diabetes, smoking ; hypercholesterolemia, previous stroke
Co-morbidities 
Medication on admission : ACE inhibitor/ARB, B-Blocker, statin , aspirin
In hospital complications : Cardiogenic shock, death, 
Acute cardiac care treatment
Triggers (Emotional/Physical)
Covid-19 +/-
Outcomes

## Takotsubo and genetics

A few case studies showed genetic polymorphism potentially involved in the pathogenesis of TS = genes coding for the adrenergic receptors (B1, B2, a2C) that could potentially involve an enhanced cardiac catecholamine sensitivity, an increased vulnerability of the heart to adrenergic stress or an impaired regulation of norepinephrine release (negative feedback impaired).

No epigenetics studies up to date. 

# How-To-Use

This app is made to run on Google Cloud Platform using Virtual Machine called App Engine. App Engine is serverless framework which automatically scales itself and handle any amount of traffic.

To know more about App Engine, check out this link(https://cloud.google.com/appengine)

Implementation can be done simply through the following steps

1. Open Cloud Shell(Terminal on Google Cloud Platform)

2. Clone this repository on Cloud Shell
```
git clone https://github.com/kwdaisuke/Takotsubo-Syndrome-Prediction-of-Hospitalization-Outcomes.git

```

3. Deploy Docker image, push it on App Engine
```
cd Takotsubo-Syndrome-Prediction-of-Hospitalization-Outcomes
make gcloud-deploy
```

`make gcloud-deploy` uses `app.yaml` file which creates App Engine and activate Dockerfile. Docker image is recorded on Container Registry and be pushed to App Engine accordingly.
