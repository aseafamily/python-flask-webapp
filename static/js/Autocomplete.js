function Autocomplete({ onCategorySelect }) {
    const [options, setOptions] = React.useState([]);
    const [inputValue, setInputValue] = React.useState('');
  
    const fetchOptions = () => {
      fetch('/categories')
        .then(response => response.json())
        .then(data => setOptions(data))
        .catch(error => console.error('Error fetching options:', error));
    };
  
    const handleInputChange = event => {
      const value = event.target.value;
      setInputValue(value);
      // Fetch options when input value changes
      fetchOptions();
    };
  
    const handleOptionSelect = option => {
      setInputValue(option);
      onCategorySelect(option); // Call the parent component's callback
    };
  
    return (
      React.createElement("div", null,
        React.createElement("ul", null,
          options.map((option, index) =>
            React.createElement("li", { key: index, onClick: () => handleOptionSelect(option) }, option)
          )
        )
      )
    );
  }
  