const title = document.title.toLowerCase();
const url = `http://localhost:5000/api/horse_odds/${title}`;

async function getData(url) {
	let res = await fetch(url);
	let data = await res.json();
	// console.log(data);

	loadDataToTable(data);

	setTimeout(getData, 3000, url);
}

function loadDataToTable(data) {
	Object.keys(data).forEach((key) => {
		if (key == "realtime") {
			const realtimeData = data[key];
			const winOdds = realtimeData["win_odds"];
			const placeOdds = realtimeData["place_odds"];
			const winHot = realtimeData["win_hot"];
			const placeHot = realtimeData["place_hot"];
			const winGreenBox = realtimeData["win_green_box"];
			const placeGreenBox = realtimeData["place_green_box"];
			const winBrownBox = realtimeData["win_brown_box"];
			const placeBrownBox = realtimeData["place_brown_box"];
			loadWinOddsToTable(winOdds, 0, winHot, winGreenBox, winBrownBox);
			loadPlaceOddsToTable(
				placeOdds,
				0,
				placeHot,
				placeGreenBox,
				placeBrownBox
			);
		} else {
			const minuteData = data[key];
			const winOdds = minuteData["win_odds"];
			const placeOdds = minuteData["place_odds"];
			const winHot = minuteData["win_hot"];
			const placeHot = minuteData["place_hot"];
			const winGreenBox = minuteData["win_green_box"];
			const placeGreenBox = minuteData["place_green_box"];
			const winBrownBox = minuteData["win_brown_box"];
			const placeBrownBox = minuteData["place_brown_box"];
			loadWinOddsToTable(winOdds, key, winHot, winGreenBox, winBrownBox);
			loadPlaceOddsToTable(
				placeOdds,
				key,
				placeHot,
				placeGreenBox,
				placeBrownBox
			);
		}
	});
}

function loadWinOddsToTable(winOdds, minute, winHot, winGreenBox, winBrownBox) {
	for (let horse = 0; horse < winOdds.length; ++horse) {
		let className;
		if (minute == 0) {
			className = "row" + (horse + 1) + " 現";
			if (winHot == horse + 1) {
				document.getElementsByClassName(
					className
				)[0].style.backgroundColor = "#C80000";
			}

			if (winGreenBox.includes((horse + 1).toString())) {
				document.getElementsByClassName(
					className
				)[0].style.backgroundColor = "#2AA216";
			}

			if (winBrownBox.includes((horse + 1).toString())) {
				document.getElementsByClassName(
					className
				)[0].style.backgroundColor = "#993300";
			}
		} else {
			className = "row" + (horse + 1) + " " + minute;
		}
		document.getElementsByClassName(className)[0].innerText =
			winOdds[horse];
	}
}

function loadPlaceOddsToTable(
	placeOdds,
	minute,
	placeHot,
	placeGreenBox,
	placeBrownBox
) {
	for (let horse = 0; horse < placeOdds.length; ++horse) {
		let className;
		if (minute == 0) {
			className = "row" + (horse + 1) + " 現";
			if (placeHot == horse + 1) {
				document.getElementsByClassName(
					className
				)[1].style.backgroundColor = "#C80000";
			}

			if (placeGreenBox.includes((horse + 1).toString())) {
				document.getElementsByClassName(
					className
				)[1].style.backgroundColor = "#2AA216";
			}

			if (placeBrownBox.includes((horse + 1).toString())) {
				document.getElementsByClassName(
					className
				)[1].style.backgroundColor = "#993300";
			}
		} else {
			className = "row" + (horse + 1) + " " + minute;
		}
		document.getElementsByClassName(className)[1].innerText =
			placeOdds[horse];
	}
}

getData(url);
