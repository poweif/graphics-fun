import webgl
from math import sin

vertex_shader_txt = """
attribute vec3 aVertexPosition;
attribute vec3 aVertexColor;
varying highp vec4 vColor;

void main(void) {
  gl_Position = vec4(aVertexPosition, 1.0);
  vColor = vec4(aVertexColor, 1.0); 
}
"""

frag_shader_txt="""
varying highp vec4 vColor;
void main(void) {
  gl_FragColor = vColor;
}
"""

gl = webgl.Context("my-canvas")
trianglesVerticeBuffer = gl.createBuffer()
trianglesColorBuffer = gl.createBuffer()
program = None

def setup():
  global program
  vs = gl.createShader(gl.VERTEX_SHADER) 
  gl.shaderSource(vs, vertext_shader_txt)
  gl.compileShader(vs)
  print "Vertex shader COMPILE_STATUS: " + str(gl.getShaderParameter(vs, gl.COMPILE_STATUS))
  fs = gl.createShader(gl.FRAGMENT_SHADER) 
  gl.shaderSource(fs, frag_shader_txt)
  gl.compileShader(fs)
  print "Fragment shader COMPILE_STATUS: " + str(gl.getShaderParameter(fs, gl.COMPILE_STATUS))

  program = gl.createProgram()
  gl.attachShader(program, vs)
  gl.attachShader(program, fs)
  gl.linkProgram(program)
  print "Program LINK_STATUS: " + str(gl.getProgramParameter(program, gl.LINK_STATUS))
  gl.useProgram(program)

  triangleVerticeColors = [1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0]

  gl.bindBuffer(gl.ARRAY_BUFFER, trianglesColorBuffer)
  gl.bufferData(gl.ARRAY_BUFFER, webgl.Float32Array(triangleVerticeColors), gl.STATIC_DRAW)

def draw(gl, elapsed):
  gl.clearColor(0.1, 0.5, 0.1, 1.0);  
  gl.clear(gl.COLOR_BUFFER_BIT);  
  gl.viewport(0, 0, 400, 300);
  translation = sin(elapsed * 2.0 * 3.14159 / 10000.0)/2.0;
  triangleVertices = [-0.5 + translation,  0.5, 0.0,
                       0.0 + translation,  0.0, 0.0,
                      -0.5 + translation, -0.5, 0.0,
                       0.5 + translation,  0.5, 0.0,
                       0.0 + translation,  0.0, 0.0,
                       0.5 + translation, -0.5, 0.0]
  gl.bindBuffer(gl.ARRAY_BUFFER, trianglesVerticeBuffer)
  gl.bufferData(gl.ARRAY_BUFFER, webgl.Float32Array(triangleVertices), gl.DYNAMIC_DRAW)
  vertexPositionAttribute = gl.getAttribLocation(program, "aVertexPosition")
  gl.enableVertexAttribArray(vertexPositionAttribute)
  gl.bindBuffer(gl.ARRAY_BUFFER, trianglesVerticeBuffer)
  gl.vertexAttribPointer(vertexPositionAttribute, 3, gl.FLOAT, False, 0, 0)

  vertexColorAttribute = gl.getAttribLocation(program, "aVertexColor")
  gl.enableVertexAttribArray(vertexColorAttribute)
  gl.bindBuffer(gl.ARRAY_BUFFER, trianglesColorBuffer)
  gl.vertexAttribPointer(vertexColorAttribute, 3, gl.FLOAT, False, 0, 0)

  gl.drawArrays(gl.TRIANGLES, 0, 6)

setup()

gl.setDrawFunc(draw);
