from sqlmodel import Session, select

from app.models.translation import Translation


def create_translation(db: Session, translation: Translation):
    db.add(translation)
    db.commit()
    db.refresh(translation)
    return translation


def get_translations_by_language(db: Session, language_code: str):
    return db.exec(
        select(Translation).where(Translation.language_code == language_code)
    ).all()


def get_translation_by_key(db: Session, language_code: str, key: str):
    return db.exec(
        select(Translation).where(
            Translation.language_code == language_code, Translation.key == key
        )
    ).first()


def update_translation(db: Session, translation_id: str, translation_data: dict):
    translation = db.get(Translation, translation_id)
    for key, value in translation_data.items():
        setattr(translation, key, value)
    db.add(translation)
    db.commit()
    db.refresh(translation)
    return translation


def delete_translation(db: Session, translation_id: str):
    translation = db.get(Translation, translation_id)
    db.delete(translation)
    db.commit()
