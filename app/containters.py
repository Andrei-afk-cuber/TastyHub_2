from app.schemas.main import UserSchema, RecipeSchema, ProductSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)