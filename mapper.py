from abc import abstractmethod

class ResponseToDomainMapper:
    @staticmethod
    @abstractmethod
    def map(v): raise NotImplementedError


class ResponseToKeySkillsMapper(ResponseToDomainMapper):
    @staticmethod
    def map(skills):
        return [k["name"] for k in skills]


class ResponseToVacancyMapper(ResponseToDomainMapper):

    @staticmethod
    def map(vacancy):
        result = {
            "id": vacancy["id"],
            "name": vacancy["name"],
            "created_at": vacancy["created_at"] or "",
            "area": vacancy["area"]["name"] or "",
            "employer": vacancy["employer"]["name"] or "",
            "experience": vacancy["experience"]["name"] or "",
            "employment": vacancy["employment"]["name"] or "",
            "schedule": vacancy["schedule"]["name"] or "",
            "description": vacancy["description"] or "",
            "responsibility": vacancy["snippet"]["responsibility"] or "",
            "requirement": vacancy["snippet"]["requirement"] or "",
            "key_skills": ResponseToKeySkillsMapper.map(vacancy["key_skills"] or [])
        }

        if vacancy["salary"] is not None:
            result["salary_from"] = vacancy["salary"]["from"] or 0.0
            result["salary_to"] = vacancy["salary"]["to"] or 0.0

        return result
