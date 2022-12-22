import spacy
from spacy.matcher import PhraseMatcher

# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp, skill_extractor = None, None
@app.on_event("startup")
def startup_event():
    global nlp, skill_extractor
    nlp = spacy.load("en_core_web_lg")
    # init skill extractor
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)


def get_skills(JD):
    """
    Get the skills fromt he Job description
    """
    # extract skills from job_description
    annotations = skill_extractor.annotate(JD)
    skills = [i['doc_node_value'] for i in annotations['results']['ngram_scored']] + [i['doc_node_value'] for i in annotations['results']['full_matches']]
    return {"skills":skills}




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/extract-skills/{jd}")
def read_item(jd: str):
    return get_skills(jd)