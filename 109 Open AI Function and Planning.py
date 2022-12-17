import openai
import base64
import requests

openai.api_key = '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'


def heading_two(text):
    code = f'<!-- wp:heading --><h2> {text}</h2><!-- /wp:heading -->'
    return code


def wp_paragrapg(text):
    code = f'<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->'
    return code


def open_ai_answer(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    output = response.get('choices')[0].get('text')
    return output


keyword = input("Enter that you are thinking: ")
prompt = f'write 7 unique questions about {keyword}'

content_one = wp_paragrapg(
    open_ai_answer(f'write a short unique SEO friendly introduction which is best match about {keyword}'))
content_two = wp_paragrapg(open_ai_answer(f'write a unique conclusion which is actually relevant about {keyword}'))
# content_img = media_file_upload('brush.jpg')

last_p = 'Conclusion'
questions = open_ai_answer(prompt)
question_list = questions.strip().split('\n')
end_line = 'Write a paragraph about it'

qna = {}
for q in question_list:
    command = f'{q} {end_line}'
    answer = open_ai_answer(command).strip().strip('\n')
    qna[q] = answer

user = 'sagor'
password = 'xhfl nwyi v4WH yptD s6T8 BGh8'
token = base64.b64encode(f'{user}:{password}'.encode())
header = {'Authorization': f'Basic {token.decode("utf-8")}'}


def wp_image(id, src, keyword):
    line_one = f'<!-- wp:image {{"align":"center","id":{id},"sizeSlug":"full","linkDestination":"none"}} -->'
    line_two = f'<figure class="wp-block-image aligncenter size-full"><img src="{src}" alt="{keyword}" class="wp-image-{id}"/>'
    line_three = f'<figcaption class="wp-element-caption">{keyword}</figcaption></figure><!-- /wp:image -->'
    code = f'{line_one}{line_two}{line_three}'
    return code


def media_file_upload(image):
    """

    :rtype: object
    """
    media_url = 'https://practice.com/wp-json/wp/v2/media'
    files = {'file': open(image, 'rb')}
    res = requests.post(media_url, files=files, headers=header)
    data = res.json()
    id = data.get('id')
    src = data.get('guid').get('rendered')
    img_code = wp_image(id, src, keyword)


# img_content = media_file_upload('brush.jpg')
content_one += media_file_upload('brush.jpg')

for key, value in qna.items():
    qn = heading_two(key).title()
    ans = wp_paragrapg(value)
    temp = qn + ans
    content_one += temp
content = f'{content_one}{heading_two(last_p)}\n{content_two}'

title = open_ai_answer(f'write a unique that is relevant to {keyword}')

data = {
    'title': title.title().replace('Q:', '').strip().strip('"'),
    'content': content,
    'slug': keyword.replace(' ', '-')
}

api_url = 'https://practice.com/wp-json/wp/v2/posts'
post = requests.post(api_url, data=data, headers=header)
print(post)
