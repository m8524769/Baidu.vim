syn match         angleParen ">"
syn match         eachKeyword "\w\+ >-\@=" contains=angleParen
hi  eachKeyword   guifg=#66D9EF             gui=italic
