import React from 'react';

export class Genre extends React.Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    const genre = e.target.value;
    this.props.onChange(genre);
  }

  render() {
    return (
      <div>
        <select
          id="genres"
          onChange={this.handleChange}>
          <option value="Pop">Pop</option>
          <option value="Jazz">Jazz</option>
          <option value="Hip Hop">Hip Hop</option>
        </select>
      </div>
    );
  }
}
