require 'rails_helper'

RSpec.describe 'API', type: :request do
  it 'returns a not found error for a non-existent item' do
    get '/api/items/999'
    expect(response).to have_http_status(404)
  end

  it 'deletes an item' do
    delete '/api/items/1'
    expect(response).to have_http_status(204)
  end
end
