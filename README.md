Database built:
User:
    - ID
    - type: admin, superstaff, staff, user
    - username: 6 <= length <= 20, lower & upper latinh and number 
    - password: 6 <= length <= 20, not copy of username
    - display name
    - email
Post:
    - ID
    - user
    - content
    - create_at
    - listCommentParent
Comment:
    - ID
    - user
    - listComment
    - reply_id
    - content
    - create_at#   b l o g  
 