# # chatbot/ai_utils.py
# import google.generativeai as genai
# from commerce_app.gemini_config import *  # Load API key

# model = genai.GenerativeModel("gemini-pro")

# # chatbot/ai_utils.py
# import google.generativeai as genai
# from gemini_config import *

# model = genai.GenerativeModel("gemini-pro")

# def get_gemini_response(user_message, product_data=None):
#     try:
#         prompt = f"""
#         User Question: {user_message}
        
#         {"Here are some product details to help you:" if product_data else ""}
#         {product_data if product_data else ""}
        
#         Provide a helpful, short, and clear response.
#         """
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"[Gemini Error]: {str(e)}"
