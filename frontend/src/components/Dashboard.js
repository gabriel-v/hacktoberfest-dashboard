import React, { Component } from 'react'
import { connect } from 'react-redux'
import { fetchParticipants } from '../actions'

import './Dashboard.css'

class Dashboard extends Component {
  componentDidMount () {
    this.props.fetchParticipants()
  }

  renderParticipant = participant => {
    const { inactive_before_event, pull_requests } = this.props.participants[
      participant
    ]
    return (
      <li key={participant}>
        {`${inactive_before_event ? 'Newcomer' : 'Veteran'} // `}
        <span className='name'>{participant}</span>
        {` // ${pull_requests.length} pull requests`}
      </li>
    )
  }

  render () {
    const { participants } = this.props
    if (!this.props.participants) return null
    let prCount = 0
    Object.values(participants).map(
      participant => (prCount += participant.pull_requests.length)
    )
    return (
      <div>
        <h1>TOTAL PULL REQUESTS: {prCount}</h1>
        <h3>Participants ranking:</h3>
        <ul>
          {Object.keys(this.props.participants)
            .sort((first, second) => {
              return (
                participants[second].pull_requests.length -
                participants[first].pull_requests.length
              )
            })
            .map(this.renderParticipant)}
        </ul>

        <h3>Latest pull requests:</h3>
        <ul>
          {/* {Object.values(this.props.participants).sort((first, second) => ).map(this.renderActivity)} */}
        </ul>
      </div>
    )
  }
}

export default connect(participants => ({ participants }), {
  fetchParticipants
})(Dashboard)
