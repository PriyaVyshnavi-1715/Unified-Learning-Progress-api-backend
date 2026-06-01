from pydantic import BaseModel, Field


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    department: str | None = Field(default=None, max_length=80)
    year: str | None = Field(default=None, max_length=30)
    goal: str | None = Field(default=None, max_length=180)


class SkillCreate(BaseModel):
    title: str = Field(min_length=2, max_length=80)
    category: str = Field(min_length=2, max_length=80)
    proficiency: int = Field(ge=0, le=100)
    target: int = Field(default=100, ge=1, le=100)
    status: str = Field(default="in-progress", pattern="^(not-started|in-progress|completed)$")
    weak_area: bool = False
    notes: str | None = Field(default=None, max_length=300)


class SkillUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=80)
    category: str | None = Field(default=None, min_length=2, max_length=80)
    proficiency: int | None = Field(default=None, ge=0, le=100)
    target: int | None = Field(default=None, ge=1, le=100)
    status: str | None = Field(default=None, pattern="^(not-started|in-progress|completed)$")
    weak_area: bool | None = None
    notes: str | None = Field(default=None, max_length=300)


class LMSProgressCreate(BaseModel):
    platform: str = Field(min_length=2, max_length=80)
    course_name: str = Field(min_length=2, max_length=120)
    completed_modules: int = Field(ge=0)
    total_modules: int = Field(gt=0)
    score: int | None = Field(default=None, ge=0, le=100)
    notes: str | None = Field(default=None, max_length=300)


class LMSProgressUpdate(BaseModel):
    platform: str | None = Field(default=None, min_length=2, max_length=80)
    course_name: str | None = Field(default=None, min_length=2, max_length=120)
    completed_modules: int | None = Field(default=None, ge=0)
    total_modules: int | None = Field(default=None, gt=0)
    score: int | None = Field(default=None, ge=0, le=100)
    notes: str | None = Field(default=None, max_length=300)


class CodingStatsCreate(BaseModel):
    platform: str = Field(min_length=2, max_length=80)
    profile_url: str | None = Field(default=None, max_length=220)
    problems_solved: int = Field(ge=0)
    contests_attended: int = Field(default=0, ge=0)
    rating: int | None = Field(default=None, ge=0)
    strongest_topic: str | None = Field(default=None, max_length=80)
    weakest_topic: str | None = Field(default=None, max_length=80)


class CodingStatsUpdate(BaseModel):
    platform: str | None = Field(default=None, min_length=2, max_length=80)
    profile_url: str | None = Field(default=None, max_length=220)
    problems_solved: int | None = Field(default=None, ge=0)
    contests_attended: int | None = Field(default=None, ge=0)
    rating: int | None = Field(default=None, ge=0)
    strongest_topic: str | None = Field(default=None, max_length=80)
    weakest_topic: str | None = Field(default=None, max_length=80)


class AssignmentCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    subject: str = Field(min_length=2, max_length=80)
    due_date: str = Field(max_length=30)
    status: str = Field(default="pending", pattern="^(pending|submitted|overdue)$")
    marks: int | None = Field(default=None, ge=0, le=100)
    notes: str | None = Field(default=None, max_length=300)


class AssignmentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=120)
    subject: str | None = Field(default=None, min_length=2, max_length=80)
    due_date: str | None = Field(default=None, max_length=30)
    status: str | None = Field(default=None, pattern="^(pending|submitted|overdue)$")
    marks: int | None = Field(default=None, ge=0, le=100)
    notes: str | None = Field(default=None, max_length=300)
