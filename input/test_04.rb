require 'rails_helper'

RSpec.describe 'API', type: :request do
  it 'returns a list of users' do
    get '/api/users'
    expect(response).to have_http_status(200)
    expect(response.body).to include('user1', 'user2')
  end

  it 'creates a user' do
    post '/api/users', params: { user: { name: 'user3', email: 'user3@example.com' } }
    expect(response).to have_http_status(201)
    expect(response.body).to include('user3')
  end
end
