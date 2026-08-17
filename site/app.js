const checkedAt = document.querySelector('#checked-at')

if (checkedAt) {
  const formatter = new Intl.DateTimeFormat('ko-KR', {
    dateStyle: 'medium',
    timeStyle: 'medium',
    timeZone: 'Asia/Seoul',
  })
  checkedAt.textContent = `${formatter.format(new Date())} KST`
}
