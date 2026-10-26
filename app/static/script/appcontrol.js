
document.addEventListener("DOMContentLoaded", () => {
    // 로그 API 주소
    const logScript = document.querySelector(
        'script[data-log-url]'
    );

    const logUrl = logScript
        ? logScript.dataset.logUrl
        : "/api/log";


    // 사용자 행동 로그 전송
    function sendLog(action, target) {
        fetch(logUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                action: action,
                target: target
            })
        }).catch((error) => {
            console.error("로그 전송 실패:", error);
        });
    }


    // 요소 식별용 이름 생성
    function getTargetName(element) {
        return (
            element.id ||
            element.name ||
            element.dataset.action ||
            element.tagName.toLowerCase()
        );
    }


    // 1. 페이지 조회 기록
    sendLog("page_view", window.location.pathname);


    // 2. 버튼 클릭 기록
    document.addEventListener("click", (event) => {
        const button = event.target.closest(
            'button, input[type="button"], ' +
            'input[type="submit"], [role="button"]'
        );

        if (button) {
            sendLog("click", getTargetName(button));
        }
    });


    // 3. 셀렉트 변경 기록
    document.addEventListener("change", (event) => {
        const element = event.target;

        if (element.matches("select")) {
            sendLog("change", getTargetName(element));
        }
    });


    // 4. 폼 제출 기록
    document.addEventListener("submit", (event) => {
        const form = event.target;

        sendLog("submit", getTargetName(form));
    });


    // 기존 #area 셀렉트 스타일 처리
    const areaSelect = document.querySelector("#area");

    if (areaSelect) {
        function updateAreaStyle() {
            if (areaSelect.value === "") {
                areaSelect.classList.add("placeholder");
            } else {
                areaSelect.classList.remove("placeholder");
            }
        }

        updateAreaStyle();
        areaSelect.addEventListener("change", updateAreaStyle);
    }
});
