package com.example.myapplication;

import android.app.ProgressDialog;
import android.os.Bundle;
//import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.textfield.TextInputEditText;

import org.json.JSONException;
import org.json.JSONObject;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;

import butterknife.ButterKnife;
import butterknife.BindView;

import static com.example.myapplication.R.style.Theme_AppCompat_Dialog;
import static com.example.myapplication.R.style.Theme_MyApplication;

public class SignupActivity extends AppCompatActivity {
    private static final String TAG = "SignupActivity";


    @BindView(R.id.input_userid) TextInputEditText _useridText;
    @BindView(R.id.input_password) TextInputEditText _passwordText;
    @BindView(R.id.input_name) TextInputEditText _nameText;
    @BindView(R.id.input_address) TextInputEditText _addressText;
    @BindView(R.id.input_contact) TextInputEditText _contactText;
    @BindView(R.id.btn_signup) Button _signupButton;
    @BindView(R.id.link_login) TextView _loginLink;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);
        ButterKnife.bind(this);
        _signupButton = (Button) findViewById(R.id.btn_signup);
        _signupButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                signup();
            }
        });
        _nameText = (TextInputEditText) findViewById((R.id.input_name));
        _useridText = (TextInputEditText) findViewById((R.id.input_userid));
        _passwordText = (TextInputEditText) findViewById((R.id.input_password));
        _addressText = (TextInputEditText) findViewById((R.id.input_address));
        _contactText = (TextInputEditText) findViewById((R.id.input_contact));
        _loginLink = (TextView) findViewById((R.id.link_login)) ;
        _loginLink.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Finish the registration screen and return to the Login activity
                finish();
            }
        });
    }

    public void signup() {
        Log.d(TAG, "Signup");

        if (!validate()) {
            onSignupFailed();
            return;
        }

        _signupButton.setEnabled(false);

        final ProgressDialog progressDialog = new ProgressDialog(SignupActivity.this,
                Theme_MyApplication);
        progressDialog.setIndeterminate(true);
        progressDialog.setMessage("Creating Account...");
        progressDialog.show();

        String name = _nameText.getText().toString();
        String userid = _useridText.getText().toString();
        String password = _passwordText.getText().toString();
        String address = _addressText.getText().toString();
        String contact = _contactText.getText().toString();
        RequestQueue requestQueue = Volley.newRequestQueue(this);
        // TODO: Implement your own signup logic here.
        String URL = "http://10.0.2.2:8000/users/" + userid + "/details";
        //DateTimeFormatter dtf = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
        //LocalDateTime now = LocalDateTime.now();
        //System.out.println(dtf.format(now));
        HashMap<String, String> params = new HashMap<String, String>();
        //params.put("query", message);
        params.put("userid",userid);
        params.put("password",password);
        params.put("name",name);
        params.put("address",address);
        params.put("contact",contact);
        JsonObjectRequest objectRequest = new JsonObjectRequest(URL, new JSONObject(params),
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            VolleyLog.v("Response to post query:%n %s", response.toString(4));
                            Log.e("rest Response",response.toString());
//                            System.out.println(response.get("response"));
                            //parsedata(response);

                        } catch (JSONException e) {
                            Log.e("resttt",e.toString());
                            e.printStackTrace();
                        }

                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                VolleyLog.e("Error: ", error.getMessage());
            }
        });

        requestQueue.add(objectRequest);
        new android.os.Handler().postDelayed(
                new Runnable() {
                    public void run() {
                        // On complete call either onSignupSuccess or onSignupFailed
                        // depending on success
                        onSignupSuccess();
                        // onSignupFailed();
                        progressDialog.dismiss();
                    }
                }, 3000);
    }


    public void onSignupSuccess() {
        _signupButton.setEnabled(true);
        setResult(RESULT_OK, null);
        finish();
    }

    public void onSignupFailed() {
        Toast.makeText(getBaseContext(), "Login failed", Toast.LENGTH_LONG).show();

        _signupButton.setEnabled(true);
    }

    public boolean validate() {
        boolean valid = true;

        String name = _nameText.getText().toString();
        String userid = _useridText.getText().toString();
        String password = _passwordText.getText().toString();
        String address = _addressText.getText().toString();
        String contact = _contactText.getText().toString();

        if (name.isEmpty() || name.length() < 3) {
            _nameText.setError("at least 3 characters");
            valid = false;
        } else {
            _nameText.setError(null);
        }

        if (userid.isEmpty()) {
            _useridText.setError("enter a valid email address");
            valid = false;
        } else {
            _useridText.setError(null);
        }

        if (password.isEmpty() || password.length() < 4 || password.length() > 10) {
            _passwordText.setError("between 4 and 10 alphanumeric characters");
            valid = false;
        } else {
            _passwordText.setError(null);
        }

        if (address.isEmpty() || address.length() < 4) {
            _addressText.setError("between 4 and 10 alphanumeric characters");
            valid = false;
        } else {
            _addressText.setError(null);
        }

        if (contact.isEmpty() || contact.length() < 10 || password.length() > 10) {
            _contactText.setError("exactly 10 digits");
            valid = false;
        } else {
            _contactText.setError(null);
        }
        return valid;
    }
}