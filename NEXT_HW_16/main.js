document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.menu button');
    const title = document.querySelector('.banner .title');
    const subtitle = document.querySelector('.banner .subtitle');

    // 초기에는 About 버튼에 해당하는 내용을 표시하고, About 버튼을 활성화 상태로 설정
    title.textContent = 'About';
    subtitle.textContent = 'Subtitle for About';
    document.querySelector('.menu button:first-child').classList.add('active');

    buttons.forEach(function (button) {
        button.addEventListener('click', function () {
            // 모든 버튼에서 active 클래스를 제거
            buttons.forEach(function (btn) {
                btn.classList.remove('active');
            });
            // 클릭된 버튼에만 active 클래스 추가
            button.classList.add('active');

            // 클릭된 버튼의 텍스트를 가져와서 제목과 부제목을 변경
            title.textContent = button.textContent;
            subtitle.textContent = 'Subtitle for ' + button.textContent;
        });
    });
});
