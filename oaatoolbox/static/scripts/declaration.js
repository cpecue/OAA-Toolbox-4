const countries = {{ majors_list|safe }};
const minors = {{ minors_list|safe }};
$(".declareBtn").click(function() {

    var declareBTN = document.getElementById('declareBtn');
    var spinner = document.getElementById('declareBTNLocation');
    spinner.innerHTML = `<button class="btn btn-lg btn-dark mb-3 btn-block" type="button" disabled>
  <span class="spinner-grow text-white" role="status" aria-hidden="true"></span>
  Declaring, wait...
</button>`;
    var advisorEmail = document.getElementById('advisorEmail').value;
    let effective_term = document.getElementById('effective_term');
    let effective_term_text = effective_term.options[effective_term.selectedIndex].text;
    var advisorPw = document.getElementById('advisorPw').value;
    var studentFN = document.getElementById('studentFN').value;
    var studentLN = document.getElementById('studentLN').value;
    var studentID = document.getElementById('studentID').value;
    var studentEmail = document.getElementById('studentEmail').value;
    var studentPhone = document.getElementById('studentPhone').value;
    let status = document.getElementById('status');
    let status_text = status.options[status.selectedIndex].text;
    var studentMajor = document.getElementById('studentMajor').value;
    var studentMinor = document.getElementById('studentMinor').value;
    index = countries.findIndex(x => x.name === studentMajor);
    test = countries[index]['Requirements'];
    majorCode = countries[index]['majorCode'];
    collegeCode = countries[index]['collegeCode'];
    degreeCode = countries[index]['degreeCode'];
    majorConcentration = countries[index]['majorConcentration'];

    $.ajax({
        url: '/_runSelenium',
        type: 'POST',
        contentType: "application/json"
        data: {collegeCode: collegeCode, majorCode: majorCode, degreeCode: degreeCode, advisorEmail: advisorEmail,
        advisorPw: advisorPw, effective_term_text: effective_term_text, studentFN: studentFN, studentLN: studentLN,
        studentID: studentID, studentEmail: studentEmail, studentPhone: studentPhone, status_text: status_text},
        success: function(response) {
            alert('Student was successfully declared! Hoo-ray!');
            location.reload();
        },
        error: function(error) {
            alert('An error has occurred, please check your approvals tab in Teams to see if it sent or not. Drat!');
        }
    });
});



var selectedSuggestionIndex = -1;
const searchInputMinors = document.querySelector('.search-input-minor');
const suggestionsPanelMinors = document.querySelector('.minorSuggestions');
const minorInput = document.querySelector('.minorModal');

const searchInput = document.querySelector('.search-input-major');
const suggestionsPanel = document.querySelector('.suggestions');
const majorInput = document.querySelector('.majorModal');

function resetSelectedSuggestion() {
  for (var i = 0; i < suggestionsPanel.children.length; i++) {
    suggestionsPanel.children[i].classList.remove('selected');
  }
}

function resetSelectedMinorsSuggestion() {
  for (var i = 0; i < suggestionsPanelMinors.children.length; i++) {
    suggestionsPanelMinors.children[i].classList.remove('selected');
  }
}

searchInput.addEventListener('keyup', function(e) {
  if (e.key === 'ArrowDown') {
    resetSelectedSuggestion();
    selectedSuggestionIndex = (selectedSuggestionIndex < suggestionsPanel.children.length - 1) ? selectedSuggestionIndex + 1 : suggestionsPanel.children.length - 1;
    suggestionsPanel.children[selectedSuggestionIndex].classList.add('selected');
    return;
  }
  if (e.key === 'ArrowUp') {
    resetSelectedSuggestion();
    selectedSuggestionIndex = (selectedSuggestionIndex > 0) ? selectedSuggestionIndex -1 : 0;
    suggestionsPanel.children[selectedSuggestionIndex].classList.add('selected');
    return;
  }
  if (e.key === 'Enter') {
    searchInput.value = suggestionsPanel.children[selectedSuggestionIndex].innerHTML;
    suggestionsPanel.classList.remove('show');
    selectedSuggestionIndex = -1;
    return;
  }
  suggestionsPanel.classList.add('show');
  const input = searchInput.value;
  suggestionsPanel.innerHTML = '';
  const suggestions = countries.filter(function(country) {
    return country.name.toLowerCase().includes(input.toLowerCase());
  });
  suggestions.forEach(function(suggested) {
    const div = document.createElement('div');
    div.innerHTML = suggested.name;
    div.setAttribute('class', 'suggestion');
    suggestionsPanel.appendChild(div);
  });
  if (input === '') {
    suggestionsPanel.innerHTML = '';
  }
});

searchInputMinors.addEventListener('keyup', function(e) {
  if (e.key === 'ArrowDown') {
    resetSelectedMinorsSuggestion();
    selectedSuggestionIndex = (selectedSuggestionIndex < suggestionsPanelMinors.children.length - 1) ? selectedSuggestionIndex + 1 : suggestionsPanelMinors.children.length - 1;
    suggestionsPanelMinors.children[selectedSuggestionIndex].classList.add('selected');
    return;
  }
  if (e.key === 'ArrowUp') {
    resetSelectedMinorsSuggestion();
    selectedSuggestionIndex = (selectedSuggestionIndex > 0) ? selectedSuggestionIndex -1 : 0;
    suggestionsPanelMinors.children[selectedSuggestionIndex].classList.add('selected');
    return;
  }
  if (e.key === 'Enter') {
    searchInputMinors.value = suggestionsPanelMinors.children[selectedSuggestionIndex].innerHTML;
    suggestionsPanelMinors.classList.remove('show');
    selectedSuggestionIndex = -1;
    return;
  }
  suggestionsPanelMinors.classList.add('show');
  const input = searchInputMinors.value;
  suggestionsPanelMinors.innerHTML = '';
  const suggestionsMinors = minors.filter(function(minor) {
    return minor.name.toLowerCase().includes(input.toLowerCase());
  });
  suggestionsMinors.forEach(function(suggested) {
    const div = document.createElement('div');
    div.innerHTML = suggested.name;
    div.setAttribute('class', 'minorSuggestions');
    suggestionsPanelMinors.appendChild(div);
  });
  if (input === '') {
    suggestionsPanelMinors.innerHTML = '';
  }
});



document.addEventListener('click', function(e) {
  if (e.target.className === 'suggestion') {
    searchInput.value = e.target.innerHTML;
<!--    suggestionsPanel.classList.remove('show');-->
    suggestionsPanel.innerHTML = '';
    return searchInput.value
  }
});

document.addEventListener('click', function(e) {
  if (e.target.className === 'minorSuggestions') {
    searchInputMinors.value = e.target.innerHTML;
    suggestionsPanelMinors.innerHTML = '';
<!--    suggestionsPanelMinors.classList.remove('show');-->
    return searchInputMinors.value
  }
});



$(function(){
  $('.majorModalBtn').click(function(e){
    e.preventDefault();
    const major = document.getElementById('studentMajor');
    document.getElementById('Major1Title').innerHTML = 'Declaration Information for ' + major.value;
    index = countries.findIndex(x => x.name === major.value);
    test = countries[index]['Requirements'];
    code = countries[index]['majorCode'];
    document.getElementById('Major1Information').innerHTML = test + '<hr />' + '<div class="badge badge-danger mr-3" style="padding:10px;">' + code + '</div>' ;

  });
})