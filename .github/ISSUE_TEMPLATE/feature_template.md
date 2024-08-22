name: Feature Template
about: 새로운 기능을 추가할 때 사용하는 템플릿
title: "[FEAT] "
labels: [enhancement]
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
        label: Description
        description: A short description of your feature. 
        placeholder: | 
          새로 추가할 기능이 무엇인지 간단하게 설명해주세요. 
        validations: 
            required: true 
    - type: markdown 
    attributes: 
        value: | 
        ### Todo 
        - [ ]
        - [ ]
