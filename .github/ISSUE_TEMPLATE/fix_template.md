name: Fix Template
about: 버그를 해결할 때 사용하는 템플릿
title: "[FIX] "
labels: [bug]
assignees: 'username'
body: 
    - type: markdown 
    attributes: 
        value: | 
            당신의 기여에 항상 감사드립니다! 
    - type: checkboxes 
    attributes: 
        label: Search before adding issue
        description: > Please search the [issues](https://github.com/Rimember/ringchat/issues) to see if a similar feature request already exists.
        options:
         - label: > I have searched the ringchat [issues]() and found no similar feature request. 
         required: true 
    - tyep: textarea 
    attributes: 
        label: Bug
        description: Provide console output with error messages and/or screenshots of the bug.
        placeholder: | 
          에러나 버그에 대한 가능한 많은 정보를 첨부해 주세요. 
        validations: 
            required: true 
    - tyep: textarea 
    attributes: 
        label: Environment
        description: Please specify the software and hardware you used to produce the bug.
        placeholder: | 
          - OS: Window 
          - Python: 3.10.6
          - Langchain: 0.2.12
        validations: 
            required: true 
