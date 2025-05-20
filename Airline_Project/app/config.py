import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://flights_db_jxxi_user:d7LAp9KQqBh86MXSlJuec1yv2BA1tQAk@dpg-d03burruibrs73838mfg-a.frankfurt-postgres.render.com/flights_db_jxxi"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")
    SWAGGER = {
        'title': 'Airline Ticketing API',
        'uiversion': 3
    }
